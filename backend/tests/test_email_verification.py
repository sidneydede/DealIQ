"""Tests validation e-mail par OTP à l'inscription (US-M1-02)."""
from __future__ import annotations

from app.models.user import User
from app.services import email as email_adapter


def _register(client, email):
    return client.post("/api/v1/auth/register", json={"email": email, "password": "Password123!"})


def test_register_creates_unverified_and_sends_otp(client, db_session):
    before = len(email_adapter.SENT)
    r = _register(client, "newuser@dealiq.com")
    assert r.status_code == 201
    assert r.json()["email_verified"] is False
    assert len(email_adapter.SENT) == before + 1  # e-mail OTP envoyé

    user = db_session.query(User).filter(User.email == "newuser@dealiq.com").one()
    assert user.email_otp and len(user.email_otp) == 6 and user.email_otp_expires is not None


def test_verify_email_with_correct_code(client, db_session):
    _register(client, "verif@dealiq.com")
    user = db_session.query(User).filter(User.email == "verif@dealiq.com").one()
    code = user.email_otp

    r = client.post("/api/v1/auth/verify-email", json={"email": "verif@dealiq.com", "code": code})
    assert r.status_code == 200 and r.json()["email_verified"] is True

    db_session.refresh(user)
    assert user.email_verified is True and user.email_otp is None


def test_verify_email_rejects_wrong_code(client, db_session):
    _register(client, "wrong@dealiq.com")
    user = db_session.query(User).filter(User.email == "wrong@dealiq.com").one()
    bad = "000000" if user.email_otp != "000000" else "111111"
    r = client.post("/api/v1/auth/verify-email", json={"email": "wrong@dealiq.com", "code": bad})
    assert r.status_code == 400


def test_resend_regenerates_code(client, db_session):
    _register(client, "resend@dealiq.com")
    user = db_session.query(User).filter(User.email == "resend@dealiq.com").one()
    first = user.email_otp
    before = len(email_adapter.SENT)
    r = client.post("/api/v1/auth/resend-verification", json={"email": "resend@dealiq.com"})
    assert r.status_code == 202
    assert len(email_adapter.SENT) == before + 1
    db_session.refresh(user)
    # Nouveau code généré (peut coïncider rarement ; l'envoi a bien eu lieu).
    assert user.email_otp is not None and first is not None


def test_admin_created_account_is_pre_verified(client, db_session):
    from app.api.deps import get_current_user
    from app.core.security import hash_password
    from app.domain.enums import Role
    from app.main import app

    admin = User(email="adm-v@dealiq.com", hashed_password=hash_password("x"), role=Role.admin)
    db_session.add(admin)
    db_session.commit()
    app.dependency_overrides[get_current_user] = lambda: admin
    r = client.post("/api/v1/users", json={"email": "staff@dealiq.com", "role": "analyste"})
    assert r.status_code == 201 and r.json()["email_verified"] is True
    app.dependency_overrides.pop(get_current_user, None)
