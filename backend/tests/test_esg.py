"""Tests M19 — ESG / impact."""
from app.api.deps import get_current_user
from app.core.security import hash_password
from app.domain.enums import Role
from app.main import app
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


def _company(client, db_session):
    entr = _user(db_session, "e@dealiq.com")
    _auth(entr)
    cid = client.post(
        "/api/v1/companies", json={"name": "Acme", "country": "CI", "sector": "Agro"}
    ).json()["company"]["id"]
    return cid, entr


_FULL = {
    "jobs_total": 50, "jobs_female": 22, "jobs_youth": 15,
    "women_in_leadership": True, "environmental_policy": True,
    "climate_risk_assessed": True, "governance_formalized": True, "board_independent": False,
}


def test_esg_requires_cabinet(client, db_session):
    cid, _ = _company(client, db_session)
    # entrepreneur ne peut pas saisir l'ESG
    assert client.put(f"/api/v1/companies/{cid}/esg", json={"jobs_total": 10}).status_code == 403
    _clear()


def test_esg_upsert_and_completeness(client, db_session):
    cid, entr = _company(client, db_session)
    _auth(_user(db_session, "a@dealiq.com", Role.analyste))
    r = client.put(f"/api/v1/companies/{cid}/esg", json={"jobs_total": 10, "jobs_female": 4})
    assert r.status_code == 200
    assert 0 < r.json()["completeness"] < 1  # partiel

    # l'entrepreneur peut lire son ESG
    _auth(entr)
    assert client.get(f"/api/v1/companies/{cid}/esg").status_code == 200
    _clear()


def test_esg_required_gating_and_full(client, db_session):
    cid, _ = _company(client, db_session)
    _auth(_user(db_session, "a@dealiq.com", Role.analyste))
    client.put(f"/api/v1/companies/{cid}/esg", json={"jobs_total": 10})
    req = client.patch(f"/api/v1/companies/{cid}/esg/required", json={"esg_required": True})
    assert req.json()["esg_required"] is True
    assert req.json()["incomplete_for_dfi"] is True  # requis mais incomplet

    full = client.put(f"/api/v1/companies/{cid}/esg", json=_FULL)
    assert full.json()["completeness"] == 1.0
    assert full.json()["incomplete_for_dfi"] is False
    _clear()


def test_esg_export(client, db_session):
    cid, _ = _company(client, db_session)
    _auth(_user(db_session, "a@dealiq.com", Role.analyste))
    client.put(f"/api/v1/companies/{cid}/esg", json=_FULL)
    exp = client.get(f"/api/v1/companies/{cid}/esg/export").json()
    assert exp["completeness"] == 1.0
    assert "impact-washing" in exp["disclaimer"]
    assert exp["indicators"]["jobs_total"] == 50
    _clear()


def test_esg_get_404_when_absent(client, db_session):
    cid, _ = _company(client, db_session)
    _auth(_user(db_session, "a@dealiq.com", Role.analyste))
    assert client.get(f"/api/v1/companies/{cid}/esg").status_code == 404
    _clear()
