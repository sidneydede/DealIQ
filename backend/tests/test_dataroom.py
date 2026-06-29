"""Tests M13 — data room (gate KYC+NDA, watermark, logs, cloisonnement)."""
import pytest

from app.api.deps import get_current_user
from app.core.security import hash_password
from app.domain.enums import AuditAction, Role
from app.main import app
from app.models.audit import AuditLog
from app.models.user import User
from app.services import documents as docsvc

PDF = ("ef.pdf", b"%PDF-1.4 contenu", "application/pdf")


@pytest.fixture(autouse=True)
def _tmp_storage(tmp_path, monkeypatch):
    monkeypatch.setattr(docsvc.settings, "storage_dir", str(tmp_path / "storage"))


def _user(db, email, role=Role.entrepreneur):
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        return existing
    u = User(email=email, hashed_password=hash_password("x"), role=role)
    db.add(u)
    db.commit()
    db.refresh(u)
    return u


def _auth(user):
    app.dependency_overrides[get_current_user] = lambda: user


def _clear():
    app.dependency_overrides.pop(get_current_user, None)


def _base(client, db_session):
    """Company investor-ready + doc + teaser publié + investisseur + intérêt (sans NDA/KYC)."""
    entr = _user(db_session, "e@dealiq.com")
    _auth(entr)
    cid = client.post(
        "/api/v1/companies", json={"name": "Clean Co", "country": "CI", "sector": "Agro"}
    ).json()["company"]["id"]
    did = client.post(
        f"/api/v1/companies/{cid}/documents",
        data={"doc_type": "etats_financiers"},
        files={"file": PDF},
    ).json()["id"]
    client.post(
        f"/api/v1/companies/{cid}/deal-type",
        json={"deal_type_primary": "ouverture_capital", "amount": 80000000},
    )
    client.post(f"/api/v1/companies/{cid}/score")

    fund = _user(db_session, "fund@dealiq.com", Role.investisseur)
    _auth(_user(db_session, "a@dealiq.com", Role.analyste))
    client.patch(f"/api/v1/companies/{cid}/status", json={"status": "investor_ready"})
    tid = client.post(f"/api/v1/companies/{cid}/teaser").json()["id"]
    client.post(f"/api/v1/teasers/{tid}/publish")
    inv_id = client.post(
        "/api/v1/investors",
        json={"name": "Sahel Capital", "type": "equity_pe_vc", "user_email": "fund@dealiq.com"},
    ).json()["id"]

    _auth(fund)
    iid = client.post(f"/api/v1/teasers/{tid}/interest", json={}).json()["id"]
    return {"cid": cid, "did": did, "inv_id": inv_id, "iid": iid, "fund": fund}


def _kyc_clear_investor(client, db_session, inv_id):
    _auth(_user(db_session, "c@dealiq.com", Role.conformite))
    client.post(
        "/api/v1/kyc/checks",
        json={"subject_type": "investor", "subject_id": inv_id, "check_type": "aml_screening"},
    )


def _cabinet(client, db_session, email="a2@dealiq.com"):
    _auth(_user(db_session, email, Role.analyste))


def test_grant_is_gated_by_kyc_then_nda(client, db_session):
    ctx = _base(client, db_session)
    _cabinet(client, db_session)
    room = client.post(f"/api/v1/companies/{ctx['cid']}/dataroom").json()
    client.post(f"/api/v1/dataroom/{room['id']}/documents", json={"document_id": ctx["did"]})

    # sans KYC -> 409
    r = client.post(f"/api/v1/dataroom/{room['id']}/access", json={"investor_id": ctx["inv_id"]})
    assert r.status_code == 409 and "KYC" in r.json()["detail"]

    # KYC ok mais NDA non signé -> 409
    _kyc_clear_investor(client, db_session, ctx["inv_id"])
    _cabinet(client, db_session)
    r = client.post(f"/api/v1/dataroom/{room['id']}/access", json={"investor_id": ctx["inv_id"]})
    assert r.status_code == 409 and "NDA" in r.json()["detail"]

    # NDA signé -> accès accordé
    client.patch(f"/api/v1/interactions/{ctx['iid']}/status", json={"status": "nda_signe"})
    r = client.post(f"/api/v1/dataroom/{room['id']}/access", json={"investor_id": ctx["inv_id"]})
    assert r.status_code == 201 and r.json()["revoked"] is False
    _clear()


def _granted_room(client, db_session, ctx):
    _kyc_clear_investor(client, db_session, ctx["inv_id"])
    _cabinet(client, db_session)
    room = client.post(f"/api/v1/companies/{ctx['cid']}/dataroom").json()
    client.post(f"/api/v1/dataroom/{room['id']}/documents", json={"document_id": ctx["did"]})
    client.patch(f"/api/v1/interactions/{ctx['iid']}/status", json={"status": "nda_signe"})
    client.post(f"/api/v1/dataroom/{room['id']}/access", json={"investor_id": ctx["inv_id"]})
    return room


def test_investor_view_has_watermark_and_logs(client, db_session):
    ctx = _base(client, db_session)
    room = _granted_room(client, db_session, ctx)

    _auth(ctx["fund"])
    rooms = client.get("/api/v1/dataroom/accessible").json()
    assert len(rooms) == 1 and rooms[0]["id"] == room["id"]

    view = client.post(
        f"/api/v1/dataroom/{room['id']}/documents/{ctx['did']}/view"
    ).json()
    assert "Sahel Capital" in view["watermark"]
    assert view["view_url"].startswith("mock-vdr://")

    # log d'accès tracé + audit
    _cabinet(client, db_session)
    logs = client.get(f"/api/v1/dataroom/{room['id']}/logs").json()
    assert len(logs) == 1 and logs[0]["action"] == "consultation"
    assert (
        db_session.query(AuditLog)
        .filter(AuditLog.action == AuditAction.dataroom_document_viewed)
        .count()
        == 1
    )
    _clear()


def test_no_access_without_grant(client, db_session):
    ctx = _base(client, db_session)
    _cabinet(client, db_session)
    room = client.post(f"/api/v1/companies/{ctx['cid']}/dataroom").json()
    client.post(f"/api/v1/dataroom/{room['id']}/documents", json={"document_id": ctx["did"]})

    _auth(ctx["fund"])
    assert client.get(f"/api/v1/dataroom/{room['id']}/documents").status_code == 403
    assert client.post(
        f"/api/v1/dataroom/{room['id']}/documents/{ctx['did']}/view"
    ).status_code == 403
    _clear()


def test_revoke_removes_access(client, db_session):
    ctx = _base(client, db_session)
    room = _granted_room(client, db_session, ctx)
    _cabinet(client, db_session)
    access = client.get(f"/api/v1/dataroom/{room['id']}/access").json()[0]
    assert client.post(f"/api/v1/dataroom/access/{access['id']}/revoke").status_code == 200

    _auth(ctx["fund"])
    assert client.get("/api/v1/dataroom/accessible").json() == []
    assert client.get(f"/api/v1/dataroom/{room['id']}/documents").status_code == 403
    _clear()


def test_partitioning_rejects_foreign_document(client, db_session):
    ctx = _base(client, db_session)
    # document d'une autre entreprise
    other = _user(db_session, "e2@dealiq.com")
    _auth(other)
    ocid = client.post(
        "/api/v1/companies", json={"name": "Other", "country": "CI", "sector": "Tech"}
    ).json()["company"]["id"]
    odid = client.post(
        f"/api/v1/companies/{ocid}/documents",
        data={"doc_type": "statuts"},
        files={"file": PDF},
    ).json()["id"]

    _cabinet(client, db_session)
    room = client.post(f"/api/v1/companies/{ctx['cid']}/dataroom").json()
    r = client.post(f"/api/v1/dataroom/{room['id']}/documents", json={"document_id": odid})
    assert r.status_code == 409  # cloisonnement
    _clear()
