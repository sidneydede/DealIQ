"""Ingestion de champs extraits (texte collé / deck) en propositions à valider.

Réutilise la même mécanique Run + Proposal que l'Agent A : l'analyste valide
ensuite champ par champ via /proposals/{id}/accept|modify|reject.
"""

import json
from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.domain.enrichment import ProposalStatus, RunStatus
from app.models.deal import Deal
from app.models.enrichment import EnrichmentProposal, EnrichmentRun
from app.services.text_extraction import ExtractedField


def ingest_extracted(
    db: Session,
    deal: Deal,
    *,
    source: str,
    label: str,
    extracted: list[ExtractedField],
) -> EnrichmentRun:
    run = EnrichmentRun(deal_id=deal.id, status=RunStatus.RUNNING)
    db.add(run)
    db.flush()

    for e in extracted:
        db.add(
            EnrichmentProposal(
                deal_id=deal.id,
                run_id=run.id,
                field=e.field,
                suggested_value=e.value,
                source=source,
                confidence=e.confidence,
                label=label,
                status=ProposalStatus.PENDING,
            )
        )

    run.status = RunStatus.DONE if extracted else RunStatus.NO_SOURCE
    run.finished_at = datetime.now(UTC)
    run.summary = json.dumps({"source": source, "n": len(extracted)}, ensure_ascii=False)

    db.commit()
    db.refresh(run)
    return run
