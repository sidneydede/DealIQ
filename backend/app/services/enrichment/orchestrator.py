"""Orchestrateur Agent A — séquence d'enrichissement étapes 1 à 7.

- Exécute chaque étape uniquement si son champ requis est renseigné.
- Respecte le délai anti rate-limit de 30 min entre deux runs sur la même fiche.
- Aucune écriture sur la fiche : produit des propositions à valider (Run + Proposals).
- Fallback total : si aucune proposition n'est produite, le run est marqué `no_source`.
"""

import json
import math
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.enrichment import (
    RATE_LIMIT_MINUTES,
    ProposalStatus,
    RunStatus,
    SourceStatus,
)
from app.models.deal import Deal
from app.models.enrichment import EnrichmentProposal, EnrichmentRun
from app.services.enrichment.base import (
    INFERABLE_FIELDS,
    EnrichmentContext,
    SourceResult,
)
from app.services.enrichment.llm import infer_llm
from app.services.enrichment.sources import SOURCE_PIPELINE

# Champs dont la présence autorise le démarrage d'Agent A (cf. CDC)
PREREQUISITE_NETWORKS = ("x_twitter", "linkedin_company", "linkedin_founder")


class RateLimited(Exception):
    def __init__(self, minutes_remaining: int):
        self.minutes_remaining = minutes_remaining
        super().__init__(f"Rate limited: {minutes_remaining} min")


class PrerequisiteNotMet(Exception):
    pass


def _now() -> datetime:
    return datetime.now(UTC)


def _aware(dt: datetime) -> datetime:
    """Normalise en UTC (les datetimes SQLite reviennent souvent naïfs)."""
    return dt if dt.tzinfo else dt.replace(tzinfo=UTC)


def _filled(value: str | None) -> bool:
    return value is not None and str(value).strip() != ""


def build_context(deal: Deal, mode: str = "mock") -> EnrichmentContext:
    socials: dict[str, list[str]] = {}
    for s in deal.socials:
        if _filled(s.value):
            socials.setdefault(s.network, []).append(s.value)
    return EnrichmentContext(
        name=deal.name,
        sector=deal.sector,
        stage=deal.stage,
        country=deal.country,
        description=deal.description,
        founders=deal.founders,
        website_url=deal.website_url,
        socials=socials,
        mode=mode,
    )


def prerequisite_met(deal: Deal) -> bool:
    if _filled(deal.website_url):
        return True
    return any(
        any(_filled(s.value) for s in deal.socials if s.network == net)
        for net in PREREQUISITE_NETWORKS
    )


def minutes_until_next(db: Session, deal_id: int) -> int:
    """0 si un enrichissement est autorisé, sinon minutes restantes."""
    last = db.execute(
        select(EnrichmentRun)
        .where(EnrichmentRun.deal_id == deal_id)
        .order_by(EnrichmentRun.started_at.desc())
        .limit(1)
    ).scalar_one_or_none()
    if last is None:
        return 0
    elapsed = (_now() - _aware(last.started_at)).total_seconds() / 60
    remaining = RATE_LIMIT_MINUTES - elapsed
    return max(0, math.ceil(remaining))


def run_enrichment(db: Session, deal: Deal, mode: str = "mock") -> EnrichmentRun:
    """Exécute Agent A. Le prérequis et le rate-limit doivent être vérifiés en amont."""
    if not prerequisite_met(deal):
        raise PrerequisiteNotMet()
    remaining = minutes_until_next(db, deal.id)
    if remaining > 0:
        raise RateLimited(remaining)

    run = EnrichmentRun(deal_id=deal.id, status=RunStatus.RUNNING)
    db.add(run)
    db.flush()  # obtenir run.id

    ctx = build_context(deal, mode=mode)
    results: list[SourceResult] = []

    # Étapes 1 à 6
    for source in SOURCE_PIPELINE:
        if not source.is_applicable(ctx):
            results.append(source.skipped())
            continue
        try:
            results.append(source.fetch(ctx))
        except Exception as exc:  # une source ne doit jamais casser le run
            results.append(
                SourceResult(code=source.code, status=SourceStatus.ERROR, label=str(exc))
            )

    proposals = [p for r in results for p in r.proposals]
    proposed_fields = {p.field for p in proposals}
    has_data = any(r.status == SourceStatus.OK for r in results)

    # Étape 7 — LLM sur les champs encore vides uniquement
    empty_inferable = [
        f
        for f in INFERABLE_FIELDS
        if not _filled(getattr(deal, f)) and f not in proposed_fields
    ]
    if has_data and empty_inferable:
        llm_result = infer_llm(ctx, empty_inferable)
        results.append(llm_result)
        proposals.extend(llm_result.proposals)

    # Signal d'activité sociale (première source qui en fournit)
    activity = next((r.activity for r in results if r.activity), None)
    if activity:
        deal.last_activity_network = activity.network
        deal.last_activity_at = activity.last_activity_at

    # Persistance des propositions (toujours en attente de validation)
    for p in proposals:
        db.add(
            EnrichmentProposal(
                deal_id=deal.id,
                run_id=run.id,
                field=p.field,
                suggested_value=p.value,
                source=p.source,
                confidence=p.confidence,
                label=p.label,
                status=ProposalStatus.PENDING,
            )
        )

    # Fallback total : aucune proposition exploitable
    run.status = RunStatus.DONE if proposals else RunStatus.NO_SOURCE
    run.finished_at = _now()
    run.summary = json.dumps(
        [
            {"source": r.code, "status": r.status, "label": r.label, "n": len(r.proposals)}
            for r in results
        ],
        ensure_ascii=False,
    )

    db.commit()
    db.refresh(run)
    return run
