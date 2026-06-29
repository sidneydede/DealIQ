"""Tests M3 — onboarding / questionnaire."""
from app.api.deps import get_current_user
from app.core.security import hash_password
from app.main import app
from app.models.user import User


def _entrepreneur(db, email="e@dealiq.com"):
    u = User(email=email, hashed_password=hash_password("x"))
    db.add(u)
    db.commit()
    db.refresh(u)
    app.dependency_overrides[get_current_user] = lambda: u
    return u


def _company_with_type(client, deal_type="ouverture_capital"):
    cid = client.post(
        "/api/v1/companies", json={"name": "Acme", "country": "CI", "sector": "Agro"}
    ).json()["company"]["id"]
    client.post(f"/api/v1/companies/{cid}/deal-type", json={"deal_type_primary": deal_type})
    return cid


def test_questionnaire_meta_has_base_and_branch(client):
    r = client.get("/api/v1/meta/questionnaire/ouverture_capital")
    assert r.status_code == 200
    ids = {q["id"] for q in r.json()}
    assert "amount" in ids  # base
    assert "dilution" in ids  # branche ouverture du capital


def test_autosave_and_resume(client, db_session):
    _entrepreneur(db_session)
    cid = _company_with_type(client)

    # session vierge créée à la volée
    s = client.get(f"/api/v1/companies/{cid}/questionnaire").json()
    assert s["answers"] == {} and s["completed"] is False

    client.put(
        f"/api/v1/companies/{cid}/questionnaire",
        json={"answers": {"stage": "Croissance"}, "current_step": 2},
    )
    # autosave fusionne, ne remplace pas
    client.put(
        f"/api/v1/companies/{cid}/questionnaire",
        json={"answers": {"amount": 50000000}, "current_step": 3},
    )
    s = client.get(f"/api/v1/companies/{cid}/questionnaire").json()
    assert s["answers"] == {"stage": "Croissance", "amount": 50000000}
    assert s["current_step"] == 3
    app.dependency_overrides.pop(get_current_user, None)


def test_submit_requires_consent(client, db_session):
    _entrepreneur(db_session)
    cid = _company_with_type(client)
    client.put(
        f"/api/v1/companies/{cid}/questionnaire",
        json={"answers": {"amount": 50000000}, "current_step": 5},
    )
    assert client.post(f"/api/v1/companies/{cid}/questionnaire/submit").status_code == 400

    c = client.post(
        f"/api/v1/companies/{cid}/questionnaire/consent",
        json={"consent_text": "J'accepte le traitement de mes données."},
    ).json()
    assert c["consent_given"] is True and c["consent_at"] is not None

    r = client.post(f"/api/v1/companies/{cid}/questionnaire/submit")
    assert r.status_code == 200
    assert r.json()["route"] == "pipeline" and r.json()["eligible"] is True
    app.dependency_overrides.pop(get_current_user, None)


def test_gating_routes_small_need_to_nurturing(client, db_session):
    _entrepreneur(db_session)
    cid = _company_with_type(client)
    client.put(
        f"/api/v1/companies/{cid}/questionnaire",
        json={"answers": {"amount": 1000000}, "current_step": 5},
    )
    client.post(
        f"/api/v1/companies/{cid}/questionnaire/consent",
        json={"consent_text": "J'accepte."},
    )
    r = client.post(f"/api/v1/companies/{cid}/questionnaire/submit").json()
    assert r["route"] == "nurturing" and r["eligible"] is False
    app.dependency_overrides.pop(get_current_user, None)
