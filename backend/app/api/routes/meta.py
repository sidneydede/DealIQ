"""Référentiels exposés au frontend (types de deal, pays, devises, secteurs, catégories)."""
from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.domain.enums import (
    Country,
    Currency,
    DealTypeCode,
    ReadinessCategory,
    currency_for_country,
    zone_for_country,
)
from app.models.reference import DealType

router = APIRouter()

_COUNTRY_LABELS = {
    Country.BJ: "Bénin", Country.BF: "Burkina Faso", Country.CI: "Côte d'Ivoire",
    Country.GW: "Guinée-Bissau", Country.ML: "Mali", Country.NE: "Niger",
    Country.SN: "Sénégal", Country.TG: "Togo", Country.CM: "Cameroun",
    Country.CF: "Centrafrique", Country.CG: "Congo", Country.GA: "Gabon",
    Country.GQ: "Guinée équatoriale", Country.TD: "Tchad",
}


@router.get("/deal-types")
def deal_types(db: Session = Depends(get_db)) -> list[dict]:
    rows = (
        db.query(DealType)
        .filter(DealType.is_active.is_(True))
        .order_by(DealType.sort_order)
        .all()
    )
    return [
        {
            "code": dt.code.value,
            "label": dt.label,
            "description": dt.description,
            "instruments": dt.instruments,
            "target_financiers": dt.target_financiers,
        }
        for dt in rows
    ]


@router.get("/countries")
def countries() -> list[dict]:
    return [
        {
            "code": c.value,
            "label": _COUNTRY_LABELS[c],
            "zone": zone_for_country(c).value,
            "currency": currency_for_country(c).value,
        }
        for c in Country
    ]


@router.get("/currencies")
def currencies() -> list[str]:
    return [c.value for c in Currency]


@router.get("/readiness-categories")
def readiness_categories() -> list[str]:
    return [c.value for c in ReadinessCategory]


@router.get("/deal-type-codes")
def deal_type_codes() -> list[str]:
    return [c.value for c in DealTypeCode]
