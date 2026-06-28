"""Seed idempotent : référentiel des types de deal + compte admin initial.

Usage : ``python -m app.seed.seed``
"""
from __future__ import annotations

import os

from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.database import SessionLocal
from app.domain.enums import Role
from app.models.reference import DealType
from app.models.user import User
from app.seed.reference_data import DEAL_TYPES


def seed_deal_types(db: Session) -> int:
    created = 0
    for data in DEAL_TYPES:
        exists = db.query(DealType).filter(DealType.code == data["code"]).first()
        if exists:
            continue
        db.add(DealType(**data))
        created += 1
    db.commit()
    return created


def seed_admin(db: Session) -> bool:
    email = os.getenv("ADMIN_EMAIL", "admin@dealiq.com")
    if db.query(User).filter(User.email == email).first():
        return False
    db.add(
        User(
            email=email,
            hashed_password=hash_password(os.getenv("ADMIN_PASSWORD", "ChangeMe123!")),
            full_name="Administrateur DealIQ",
            role=Role.admin,
        )
    )
    db.commit()
    return True


def main() -> None:
    db = SessionLocal()
    try:
        n = seed_deal_types(db)
        admin = seed_admin(db)
        print(f"Seed terminé : {n} type(s) de deal créé(s) ; admin créé={admin}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
