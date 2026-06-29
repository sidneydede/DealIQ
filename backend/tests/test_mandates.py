"""Tests M17 — mandats & honoraires + registre des conflits."""
from app.api.deps import get_current_user
from app.core.security import hash_password
from app.domain.enums import AuditAction, Role
from app.main import app
from app.models.audit import AuditLog
from app.models.user import User


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


def _company(client, name="Acme"):
    return client.post(
        "/api/v1/companies", json={"name": name, "country": "CI", "sector": "Agro"}
    ).json()["company"]["id"]


def test_create_mandate_requires_cabinet(client, db_session):
    _auth(_user(db_session, "e@dealiq.com"))
    cid = _company(client)
    # entrepreneur interdit
    r = client.post(
        f"/api/v1/companies/{cid}/mandates",
        json={"represented_party": "entreprise", "mandate_type": "levee"},
    )
    assert r.status_code == 403
    _clear()


def test_mandate_and_fee_flow(client, db_session):
    _auth(_user(db_session, "e@dealiq.com"))
    cid = _company(client)

    _auth(_user(db_session, "s@dealiq.com", Role.senior))
    m = client.post(
        f"/api/v1/companies/{cid}/mandates",
        json={"represented_party": "entreprise", "mandate_type": "levee", "exclusive": True},
    )
    assert m.status_code == 201 and m.json()["represented_party"] == "entreprise"
    mid = m.json()["id"]
    assert (
        db_session.query(AuditLog).filter(AuditLog.action == AuditAction.mandate_created).count()
        == 1
    )

    # signature + activation
    upd = client.patch(f"/api/v1/mandates/{mid}", json={"status": "actif", "signed": True})
    assert upd.status_code == 200 and upd.json()["signed"] is True
    assert (
        db_session.query(AuditLog)
        .filter(AuditLog.action == AuditAction.mandate_status_changed)
        .count()
        == 1
    )

    # honoraires
    fee = client.post(
        f"/api/v1/mandates/{mid}/fees",
        json={"fee_type": "success_fee", "amount": 5000000, "currency": "XOF"},
    )
    assert fee.status_code == 201 and fee.json()["status"] == "du"
    fid = fee.json()["id"]
    assert len(client.get(f"/api/v1/mandates/{mid}/fees").json()) == 1

    paid = client.patch(f"/api/v1/fees/{fid}", json={"status": "paye"})
    assert paid.status_code == 200 and paid.json()["status"] == "paye"
    _clear()


def test_conflict_register_flags_double_mandate(client, db_session):
    _auth(_user(db_session, "e@dealiq.com"))
    cid = _company(client, "Conflit Co")

    _auth(_user(db_session, "s@dealiq.com", Role.senior))
    client.post(
        f"/api/v1/companies/{cid}/mandates",
        json={"represented_party": "entreprise", "mandate_type": "levee"},
    )
    client.post(
        f"/api/v1/companies/{cid}/mandates",
        json={"represented_party": "investisseur", "mandate_type": "sourcing"},
    )

    # registre des conflits réservé à la gouvernance (conformité/senior/admin)
    _auth(_user(db_session, "an@dealiq.com", Role.analyste))
    assert client.get("/api/v1/conflicts").status_code == 403

    _auth(_user(db_session, "c@dealiq.com", Role.conformite))
    register = client.get("/api/v1/conflicts").json()
    item = next(i for i in register if i["company_id"] == cid)
    assert item["has_conflict"] is True
    assert item["disclosure"] is not None
    assert set(item["represented_parties"]) == {"entreprise", "investisseur"}
    _clear()
