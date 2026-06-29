"""Service teaser (M11) & interactions / mise en relation (M12)."""
from __future__ import annotations

from sqlalchemy.orm import Session

from app.domain import teaser as anon
from app.domain.enums import (
    AuditAction,
    Instrument,
    InteractionStatus,
    TeaserStatus,
    zone_for_country,
)
from app.models.company import Company
from app.models.investor import Investor
from app.models.reference import DealType
from app.models.teaser import Interaction, Teaser
from app.models.user import User
from app.services import audit

# Dimensions fortes → points forts anonymisés du teaser.
_STRENGTH_LABELS = {
    "traction": "Traction commerciale",
    "profitabilite_cashflow": "Profil de cash-flow",
    "qualite_info_financiere": "Information financière fiable",
    "gouvernance": "Gouvernance structurée",
    "qualite_documentaire": "Dossier bien documenté",
}


def _strengths(company: Company) -> list[str]:
    score = company.score
    if not score or not score.subscores:
        return ["Dossier préparé par le Cabinet"]
    strong = sorted(
        ((d, v) for d, v in score.subscores.items() if v >= 0.6 and d in _STRENGTH_LABELS),
        key=lambda kv: kv[1],
        reverse=True,
    )
    labels = [_STRENGTH_LABELS[d] for d, _ in strong[:3]]
    return labels or ["Dossier préparé par le Cabinet"]


def generate(db: Session, company: Company, actor: User) -> Teaser:
    """Génère (ou régénère) un teaser anonymisé en brouillon depuis une fiche."""
    need = company.financing_need
    deal_type = need.deal_type_primary if need else None
    dt = (
        db.query(DealType).filter(DealType.code == deal_type).first()
        if deal_type is not None
        else None
    )
    instrument = Instrument(dt.instruments[0]) if dt and dt.instruments else None
    zone = zone_for_country(company.country)
    revenue = company.revenue_max or company.revenue_min

    existing = db.query(Teaser).filter(Teaser.company_id == company.id).first()
    teaser = existing or Teaser(company_id=company.id, version=0)
    teaser.deal_type = deal_type
    teaser.template = dt.teaser_template if dt else None
    teaser.title = anon.build_title(company.sector, zone, deal_type)
    teaser.sector = company.sector
    teaser.zone = zone.value
    teaser.revenue_band = anon.band(float(revenue) if revenue is not None else None)
    teaser.amount_band = anon.band(float(need.amount) if need and need.amount is not None else None)
    teaser.instrument = instrument
    teaser.strengths = _strengths(company)
    teaser.summary = (
        f"Opportunité {anon.zone_label(zone)} dans le secteur {company.sector}, "
        f"préparée et validée par le Cabinet."
    )
    teaser.version = (teaser.version or 0) + 1
    teaser.status = TeaserStatus.brouillon  # toute régénération repasse en validation
    if existing is None:
        db.add(teaser)
    db.commit()
    db.refresh(teaser)
    return teaser


def publish(db: Session, teaser: Teaser, actor: User, ip: str | None = None) -> Teaser:
    teaser.status = TeaserStatus.publie
    teaser.validated_by = actor.id
    db.commit()
    db.refresh(teaser)
    audit.record(
        db, AuditAction.teaser_published, actor=actor, object_type="Teaser",
        object_id=teaser.id, meta={"company_id": teaser.company_id}, ip_address=ip,
    )
    return teaser


def get_by_company(db: Session, company: Company) -> Teaser | None:
    return db.query(Teaser).filter(Teaser.company_id == company.id).first()


def list_published(
    db: Session,
    *,
    instrument: str | None = None,
    deal_type: str | None = None,
    sector: str | None = None,
    zone: str | None = None,
) -> list[Teaser]:
    q = db.query(Teaser).filter(Teaser.status == TeaserStatus.publie)
    if instrument:
        q = q.filter(Teaser.instrument == instrument)
    if deal_type:
        q = q.filter(Teaser.deal_type == deal_type)
    if sector:
        q = q.filter(Teaser.sector == sector)
    if zone:
        q = q.filter(Teaser.zone == zone)
    return q.order_by(Teaser.created_at.desc()).all()


# --- M12 : intérêt & mise en relation ---
def express_interest(
    db: Session, teaser: Teaser, investor: Investor, note: str | None, actor: User,
    ip: str | None = None,
) -> Interaction:
    existing = (
        db.query(Interaction)
        .filter(Interaction.teaser_id == teaser.id, Interaction.investor_id == investor.id)
        .first()
    )
    if existing:
        return existing
    interaction = Interaction(
        teaser_id=teaser.id,
        company_id=teaser.company_id,
        investor_id=investor.id,
        note=note,
        status=InteractionStatus.interesse,
    )
    db.add(interaction)
    db.commit()
    db.refresh(interaction)
    audit.record(
        db, AuditAction.interaction_created, actor=actor, object_type="Interaction",
        object_id=interaction.id, meta={"teaser_id": teaser.id}, ip_address=ip,
    )
    return interaction


def update_interaction_status(
    db: Session, interaction: Interaction, new_status: InteractionStatus, actor: User,
    ip: str | None = None,
) -> Interaction:
    old = interaction.status
    interaction.status = new_status
    db.commit()
    db.refresh(interaction)
    audit.record(
        db, AuditAction.interaction_status_changed, actor=actor, object_type="Interaction",
        object_id=interaction.id, meta={"old": old.value, "new": new_status.value}, ip_address=ip,
    )
    return interaction
