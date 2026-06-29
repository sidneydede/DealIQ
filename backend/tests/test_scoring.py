"""Tests Lot 3 — M5 (readiness), M6 (rapport), M7 (offres/devis)."""
from app.api.deps import get_current_user
from app.core.security import hash_password
from app.domain.enums import AuditAction, Role
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


def _company(client, deal_type="ouverture_capital"):
    cid = client.post(
        "/api/v1/companies", json={"name": "Acme", "country": "CI", "sector": "Agro"}
    ).json()["company"]["id"]
    client.post(
        f"/api/v1/companies/{cid}/deal-type",
        json={"deal_type_primary": deal_type, "amount": 80000000, "use_of_funds": "Croissance"},
    )
    return cid


def _clear():
    app.dependency_overrides.pop(get_current_user, None)


def test_entrepreneur_view_hides_raw_score(client, db_session):
    entr = _user(db_session, "e@dealiq.com")
    _auth(entr)
    cid = _company(client)
    r = client.post(f"/api/v1/companies/{cid}/score")
    assert r.status_code == 200
    body = r.json()
    assert "category" in body and "gaps" in body
    assert "total" not in body and "subscores" not in body  # RG-M5-04
    assert db_session.query(AuditLog).filter(
        AuditLog.action == AuditAction.score_computed
    ).count() == 1
    _clear()


def test_cabinet_view_shows_full_score(client, db_session):
    entr = _user(db_session, "e@dealiq.com")
    _auth(entr)
    cid = _company(client)
    client.post(f"/api/v1/companies/{cid}/score")

    _auth(_user(db_session, "analyste@dealiq.com", Role.analyste))
    r = client.get(f"/api/v1/companies/{cid}/score")
    assert r.status_code == 200
    body = r.json()
    assert "total" in body and "subscores" in body
    assert body["category"] is not None
    _clear()


def test_no_investor_ready_without_verified_financials(client, db_session):
    _auth(_user(db_session, "e@dealiq.com"))
    cid = _company(client)
    cat = client.post(f"/api/v1/companies/{cid}/score").json()["category"]
    assert cat != "investor_ready"  # gating documentaire (RG-M5-01)
    _clear()


def test_investor_cannot_access_score(client, db_session):
    _auth(_user(db_session, "e@dealiq.com"))
    cid = _company(client)
    _auth(_user(db_session, "inv@dealiq.com", Role.investisseur))
    assert client.post(f"/api/v1/companies/{cid}/score").status_code == 403
    _clear()


def test_report_content(client, db_session):
    _auth(_user(db_session, "e@dealiq.com"))
    cid = _company(client, deal_type="ouverture_capital")
    r = client.get(f"/api/v1/companies/{cid}/report")
    assert r.status_code == 200
    body = r.json()
    assert body["category_label"]
    assert "equity" in body["recommended_instrument"].lower()
    assert isinstance(body["blockers"], list)
    assert any("garantie de financement" in d for d in body["disclaimers"])
    _clear()


def test_report_requires_deal_type(client, db_session):
    _auth(_user(db_session, "e@dealiq.com"))
    cid = client.post(
        "/api/v1/companies", json={"name": "NoType", "country": "CI", "sector": "Agro"}
    ).json()["company"]["id"]
    assert client.get(f"/api/v1/companies/{cid}/report").status_code == 400
    _clear()


def test_offers_have_no_price_and_anti_p2p(client, db_session):
    _auth(_user(db_session, "e@dealiq.com"))
    r = client.get("/api/v1/meta/offers")
    assert r.status_code == 200
    body = r.json()
    assert "qualité de votre dossier" in body["anti_pay_to_play"]
    pricings = {o["pricing"] for o in body["offers"]}
    assert pricings <= {"gratuit", "ticket_engagement", "sur_devis"}
    # aucun champ de montant exposé
    for o in body["offers"]:
        assert set(o.keys()) == {"key", "label", "pricing", "deliverables"}
    _clear()


def test_quote_request_flow(client, db_session):
    _auth(_user(db_session, "e@dealiq.com"))
    cid = _company(client)
    r = client.post(
        f"/api/v1/companies/{cid}/quote-request",
        json={"offer_key": "preparation", "message": "Je souhaite un devis.",
              "contact_phone": "+2250700000000"},
    )
    assert r.status_code == 201
    assert r.json()["status"] == "nouveau"
    assert r.json()["deal_type"] == "ouverture_capital"

    # vue cabinet : toutes les demandes
    _auth(_user(db_session, "senior@dealiq.com", Role.senior))
    allq = client.get("/api/v1/quote-requests").json()
    assert len(allq) == 1
    _clear()
