"""Seed idempotent : données de référence CI/UEMOA + premier analyste.

Usage : python -m app.seed.seed
Sûr à relancer : n'insère que les lignes manquantes.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import settings
from app.core.security import hash_password
from app.database import SessionLocal
from app.models.reference import (
    Accelerator,
    Country,
    DealSourceType,
    Fund,
    Sector,
)
from app.models.user import User
from app.seed import reference_data as ref


def _seed_countries(db: Session) -> int:
    existing = {row[0] for row in db.execute(select(Country.iso2)).all()}
    added = 0
    for iso2, name, is_uemoa in ref.COUNTRIES:
        if iso2 not in existing:
            db.add(Country(iso2=iso2, name=name, is_uemoa=is_uemoa))
            added += 1
    return added


def _seed_simple(db: Session, model, names: list[str], field: str = "name") -> int:
    existing = {row[0] for row in db.execute(select(getattr(model, field))).all()}
    added = 0
    for name in names:
        if name not in existing:
            db.add(model(**{field: name}))
            added += 1
    return added


def _seed_pairs(db: Session, model, pairs, key_field, val_field) -> int:
    existing = {row[0] for row in db.execute(select(getattr(model, key_field))).all()}
    added = 0
    for key, val in pairs:
        if key not in existing:
            db.add(model(**{key_field: key, val_field: val}))
            added += 1
    return added


def _seed_first_user(db: Session) -> bool:
    exists = db.execute(
        select(User).where(User.email == settings.first_user_email)
    ).scalar_one_or_none()
    if exists:
        return False
    db.add(
        User(
            email=settings.first_user_email,
            full_name="Analyste DealIQ",
            hashed_password=hash_password(settings.first_user_password),
            is_active=True,
        )
    )
    return True


def run() -> None:
    db = SessionLocal()
    try:
        report = {
            "countries": _seed_countries(db),
            "sectors": _seed_simple(db, Sector, ref.SECTORS),
            "funds": _seed_pairs(db, Fund, ref.FUNDS, "name", "country"),
            "accelerators": _seed_pairs(
                db, Accelerator, ref.ACCELERATORS, "name", "country"
            ),
            "deal_source_types": _seed_pairs(
                db, DealSourceType, ref.DEAL_SOURCE_TYPES, "code", "label"
            ),
            "first_user_created": _seed_first_user(db),
        }
        db.commit()
        print("Seed terminé :", report)
    finally:
        db.close()


if __name__ == "__main__":
    run()
