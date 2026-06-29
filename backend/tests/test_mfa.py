"""Tests MFA/TOTP : enrôlement, activation, login en deux étapes, désactivation."""
from __future__ import annotations

import pyotp


def _register_login(client, email):
    client.post("/api/v1/auth/register", json={"email": email, "password": "Password123!"})
    r = client.post("/api/v1/auth/login", json={"email": email, "password": "Password123!"}).json()
    return {"Authorization": f"Bearer {r['access_token']}"}


def _enroll(client, headers):
    secret = client.post("/api/v1/auth/mfa/setup", headers=headers).json()["secret"]
    code = pyotp.TOTP(secret).now()
    r = client.post("/api/v1/auth/mfa/enable", json={"code": code}, headers=headers)
    assert r.status_code == 200 and r.json()["mfa_enabled"] is True
    return secret


def _wrong(secret):
    real = pyotp.TOTP(secret).now()
    return "000000" if real != "000000" else "111111"


def test_setup_returns_otpauth_uri(client):
    h = _register_login(client, "mfa-setup@dealiq.com")
    setup = client.post("/api/v1/auth/mfa/setup", headers=h).json()
    assert setup["secret"]
    assert setup["otpauth_uri"].startswith("otpauth://totp/")
    assert "DealIQ" in setup["otpauth_uri"]


def test_enable_then_two_step_login(client):
    h = _register_login(client, "mfa-login@dealiq.com")
    secret = _enroll(client, h)

    # Le login renvoie désormais un défi, pas de jetons.
    login = client.post(
        "/api/v1/auth/login",
        json={"email": "mfa-login@dealiq.com", "password": "Password123!"},
    ).json()
    assert login["mfa_required"] is True
    assert login["access_token"] is None and login["mfa_token"]

    # Code valide -> jetons.
    code = pyotp.TOTP(secret).now()
    verified = client.post(
        "/api/v1/auth/mfa/verify", json={"mfa_token": login["mfa_token"], "code": code}
    )
    assert verified.status_code == 200 and verified.json()["access_token"]


def test_enable_rejects_wrong_code(client):
    h = _register_login(client, "mfa-bad@dealiq.com")
    secret = client.post("/api/v1/auth/mfa/setup", headers=h).json()["secret"]
    r = client.post("/api/v1/auth/mfa/enable", json={"code": _wrong(secret)}, headers=h)
    assert r.status_code == 400


def test_verify_rejects_wrong_code(client):
    h = _register_login(client, "mfa-badverify@dealiq.com")
    secret = _enroll(client, h)
    login = client.post(
        "/api/v1/auth/login",
        json={"email": "mfa-badverify@dealiq.com", "password": "Password123!"},
    ).json()
    bad = client.post(
        "/api/v1/auth/mfa/verify",
        json={"mfa_token": login["mfa_token"], "code": _wrong(secret)},
    )
    assert bad.status_code == 401


def test_disable_returns_to_single_step(client):
    h = _register_login(client, "mfa-disable@dealiq.com")
    secret = _enroll(client, h)
    r = client.post(
        "/api/v1/auth/mfa/disable", json={"code": pyotp.TOTP(secret).now()}, headers=h
    )
    assert r.status_code == 200 and r.json()["mfa_enabled"] is False

    login = client.post(
        "/api/v1/auth/login",
        json={"email": "mfa-disable@dealiq.com", "password": "Password123!"},
    ).json()
    assert login["mfa_required"] is False and login["access_token"]


def test_setup_conflict_when_already_enabled(client):
    h = _register_login(client, "mfa-twice@dealiq.com")
    _enroll(client, h)
    assert client.post("/api/v1/auth/mfa/setup", headers=h).status_code == 400
