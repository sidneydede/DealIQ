"""Codes OTP de validation e-mail (US-M1-02)."""
from __future__ import annotations

import secrets
from datetime import UTC, datetime, timedelta

OTP_TTL_MINUTES = 15


def generate_code() -> str:
    """Code numérique à 6 chiffres (zéros de tête conservés)."""
    return f"{secrets.randbelow(1_000_000):06d}"


def expiry() -> datetime:
    return datetime.now(UTC) + timedelta(minutes=OTP_TTL_MINUTES)


def is_valid(stored: str | None, expires: datetime | None, code: str) -> bool:
    if not stored or expires is None:
        return False
    exp = expires if expires.tzinfo else expires.replace(tzinfo=UTC)
    if exp < datetime.now(UTC):
        return False
    return secrets.compare_digest(stored, code.strip())
