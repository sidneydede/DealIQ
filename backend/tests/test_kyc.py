"""Tests M15 — KYC/KYB/AML (adaptateur mock)."""
from app.api.deps import get_current_user
from app.core.security import hash_password
from app.domain import kyc as provider
from app.domain.enums import AuditAction, KycCheckType, KycStatus, Role
from app.main import app
from app.models.audit import AuditLog
from app.models.user import User


def _user(db, email, role=Role.entrepreneur):
    u = User(email=email, hashed_password=hash_password("x"), role=role)
    db.add(u)
    db.commit()
    db.refresh(u)
    return u


def _auth(user):
    app.dependency_overrides[get_current_user] = lambda: user


def _clear():
    app.dependency_overrides.pop(get_current_user, None)


def _company(client, name):
    return client.post(
        "/api/v1/companies", json={"name": name, "country": "CI", "sector": "Agro"}
    ).json()["company"]["id"]


# --- domaine pur (mock) ---
def test_mock_provider():
    assert provider.run_mock("Clean SARL", KycCheckType.aml_screening)[0] == KycStatus.valide
    st, res = provider.run_mock("Sanction Corp", KycCheckType.aml_screening)
    assert st == KycStatus.hit and res["sanctions"] is True
    st2, res2 = provider.run_mock("A PEP holding", KycCheckType.aml_screening)
    assert st2 == KycStatus.hit and res2["pep"] is True
    assert provider.run_mock("Fraud Ltd", KycCheckType.kyb)[0] == KycStatus.rejete
    assert provider.run_mock("Honest SA", KycCheckType.kyb)[0] == KycStatus.valide


# --- RBAC ---
def test_kyc_requires_conformite(client, db_session):
    _auth(_user(db_session, "e@dealiq.com"))
    cid = _company(client, "Clean SARL")
    # entrepreneur interdit
    r = client.post(
        "/api/v1/kyc/checks",
        json={"subject_type": "company", "subject_id": cid, "check_type": "kyb"},
    )
    assert r.status_code == 403
    # analyste interdit aussi (réservé conformité/admin)
    _auth(_user(db_session, "a@dealiq.com", Role.analyste))
    assert client.get("/api/v1/kyc/checks").status_code == 403
    _clear()


# --- workflow ---
def test_kyb_valid_then_cleared(client, db_session):
    _auth(_user(db_session, "e@dealiq.com"))
    cid = _company(client, "Honest SA")
    _auth(_user(db_session, "c@dealiq.com", Role.conformite))
    r = client.post(
        "/api/v1/kyc/checks",
        json={"subject_type": "company", "subject_id": cid, "check_type": "kyb"},
    )
    assert r.status_code == 201 and r.json()["status"] == "valide"
    assert r.json()["result"]["beneficial_owners"] == "identifiés"

    cleared = client.get(f"/api/v1/kyc/subjects/company/{cid}/cleared").json()
    assert cleared["cleared"] is True
    _clear()


def test_sanction_hit_alerts_and_blocks(client, db_session):
    _auth(_user(db_session, "e@dealiq.com"))
    cid = _company(client, "Sanction Corp")
    _auth(_user(db_session, "c@dealiq.com", Role.conformite))
    r = client.post(
        "/api/v1/kyc/checks",
        json={"subject_type": "company", "subject_id": cid, "check_type": "aml_screening"},
    )
    assert r.status_code == 201 and r.json()["status"] == "hit"

    # alerte conformité tracée
    assert (
        db_session.query(AuditLog)
        .filter(AuditLog.action == AuditAction.kyc_hit_alert)
        .count()
        == 1
    )
    # un hit bloque le « cleared »
    assert client.get(f"/api/v1/kyc/subjects/company/{cid}/cleared").json()["cleared"] is False
    _clear()


def test_manual_status_override_is_audited(client, db_session):
    _auth(_user(db_session, "e@dealiq.com"))
    cid = _company(client, "Honest SA")
    conf = _user(db_session, "c@dealiq.com", Role.conformite)
    _auth(conf)
    check_id = client.post(
        "/api/v1/kyc/checks",
        json={"subject_type": "company", "subject_id": cid, "check_type": "manuelle"},
    ).json()["id"]

    r = client.patch(
        f"/api/v1/kyc/checks/{check_id}",
        json={"status": "valide", "notes": "Pièces vérifiées en séance."},
    )
    assert r.status_code == 200 and r.json()["status"] == "valide"
    assert r.json()["checked_by"] == conf.id
    assert (
        db_session.query(AuditLog)
        .filter(AuditLog.action == AuditAction.kyc_status_changed)
        .count()
        == 1
    )
    _clear()
