"""TOTP (MFA) — génération de secret, URI d'enrôlement et vérification de code.

Compatible Google Authenticator / Microsoft Authenticator / etc. (RFC 6238).
"""
from __future__ import annotations

import pyotp

ISSUER = "DealIQ"


def generate_secret() -> str:
    return pyotp.random_base32()


def provisioning_uri(secret: str, account: str) -> str:
    """URI otpauth:// à encoder en QR code côté client."""
    return pyotp.TOTP(secret).provisioning_uri(name=account, issuer_name=ISSUER)


def verify(secret: str, code: str) -> bool:
    if not secret or not code:
        return False
    # valid_window=1 : tolère un pas de temps (±30 s) pour les horloges désynchronisées.
    return pyotp.TOTP(secret).verify(code.strip().replace(" ", ""), valid_window=1)
