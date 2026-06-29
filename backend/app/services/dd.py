"""Service DD OHADA/SYSCOHADA (M18)."""
from __future__ import annotations

from sqlalchemy.orm import Session

from app.domain import syscohada
from app.domain.enums import AuditAction
from app.models.company import Company
from app.models.dd import DdAnalysis, SyscohadaImport
from app.models.user import User
from app.services import audit


class DdError(Exception):
    """Erreur de DD (ex. aucune balance importée)."""


def import_balance(db: Session, company: Company, data, actor: User) -> SyscohadaImport:
    version = (
        db.query(SyscohadaImport).filter(SyscohadaImport.company_id == company.id).count() + 1
    )
    imp = SyscohadaImport(
        company_id=company.id,
        fiscal_year=data.fiscal_year,
        lines=[line.model_dump() for line in data.lines],
        version=version,
        imported_by=actor.id,
    )
    db.add(imp)
    db.commit()
    db.refresh(imp)
    return imp


def latest_import(db: Session, company: Company) -> SyscohadaImport | None:
    return (
        db.query(SyscohadaImport)
        .filter(SyscohadaImport.company_id == company.id)
        .order_by(SyscohadaImport.version.desc())
        .first()
    )


def compute(db: Session, company: Company, actor: User, ip: str | None = None) -> DdAnalysis:
    imp = latest_import(db, company)
    if imp is None:
        raise DdError("Aucune balance SYSCOHADA importée.")

    deal_type = company.financing_need.deal_type_primary if company.financing_need else None
    lines = imp.lines or []

    analysis = DdAnalysis(
        company_id=company.id,
        import_id=imp.id,
        deal_type=deal_type,
        class_totals=syscohada.class_totals(lines),
        retraitements=syscohada.retraitements(lines),
        focus=syscohada.dd_focus(deal_type),
        grid_version=syscohada.SYSCOHADA_VERSION,
    )
    analysis.synthesis = syscohada.synthesis(analysis.retraitements, deal_type)
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    audit.record(
        db, AuditAction.dd_computed, actor=actor, object_type="Company", object_id=company.id,
        meta={"import_version": imp.version, "grid": syscohada.SYSCOHADA_VERSION},
        ip_address=ip,
    )
    return analysis


def latest_analysis(db: Session, company: Company) -> DdAnalysis | None:
    return (
        db.query(DdAnalysis)
        .filter(DdAnalysis.company_id == company.id)
        .order_by(DdAnalysis.created_at.desc())
        .first()
    )
