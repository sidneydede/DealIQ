"""Tests V1-A — M9 (investisseurs/critères) et M10 (matching)."""
from app.api.deps import get_current_user
from app.core.security import hash_password
from app.domain import matching
from app.domain.enums import Role
from app.main import app
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


def _criteria(**over):
    base = {
        "countries": ["CI"], "sectors": ["Agro"], "instruments": ["equity"],
        "deal_types": ["ouverture_capital"], "stages": [], "exclusions": [],
        "ticket_min": 10000000, "ticket_max": 200000000, "ticket_currency": "XOF",
        "esg_required": False,
    }
    base.update(over)
    return base


# --- M9 ---
def test_investor_crud_and_link(client, db_session):
    inv_user = _user(db_session, "fund@dealiq.com", Role.investisseur)
    _auth(_user(db_session, "a@dealiq.com", Role.analyste))
    r = client.post(
        "/api/v1/investors",
        json={"name": "Sahel Capital", "type": "equity_pe_vc", "user_email": "fund@dealiq.com"},
    )
    assert r.status_code == 201
    assert r.json()["user_id"] == inv_user.id

    # investisseur voit sa fiche via /me
    _auth(inv_user)
    me = client.get("/api/v1/investors/me")
    assert me.status_code == 200 and me.json()["name"] == "Sahel Capital"
    _clear()


def test_investor_only_sees_own(client, db_session):
    inv_user = _user(db_session, "fund@dealiq.com", Role.investisseur)
    _auth(_user(db_session, "a@dealiq.com", Role.analyste))
    client.post("/api/v1/investors", json={"name": "A", "type": "banque"})
    client.post(
        "/api/v1/investors",
        json={"name": "B", "type": "equity_pe_vc", "user_email": "fund@dealiq.com"},
    )
    assert len(client.get("/api/v1/investors").json()) == 2

    _auth(inv_user)
    own = client.get("/api/v1/investors").json()
    assert len(own) == 1 and own[0]["name"] == "B"
    _clear()


def test_criteria_set_by_owner(client, db_session):
    inv_user = _user(db_session, "fund@dealiq.com", Role.investisseur)
    _auth(_user(db_session, "a@dealiq.com", Role.analyste))
    inv_id = client.post(
        "/api/v1/investors",
        json={"name": "B", "type": "equity_pe_vc", "user_email": "fund@dealiq.com"},
    ).json()["id"]

    _auth(inv_user)
    r = client.put(f"/api/v1/investors/{inv_id}/criteria", json=_criteria())
    assert r.status_code == 200 and r.json()["deal_types"] == ["ouverture_capital"]
    _clear()


# --- M10 ---
def _ready_company(client):
    cid = client.post(
        "/api/v1/companies", json={"name": "Acme", "country": "CI", "sector": "Agro"}
    ).json()["company"]["id"]
    client.post(
        f"/api/v1/companies/{cid}/deal-type",
        json={"deal_type_primary": "ouverture_capital", "amount": 80000000},
    )
    return cid


def test_matching_requires_investor_ready(client, db_session):
    entr = _user(db_session, "e@dealiq.com")
    _auth(entr)
    cid = _ready_company(client)
    _auth(_user(db_session, "a@dealiq.com", Role.analyste))
    # pas encore investor-ready -> 409
    assert client.get(f"/api/v1/companies/{cid}/matches").status_code == 409
    _clear()


def test_matching_filters_and_fit(client, db_session):
    entr = _user(db_session, "e@dealiq.com")
    _auth(entr)
    cid = _ready_company(client)

    cab = _user(db_session, "a@dealiq.com", Role.analyste)
    _auth(cab)
    client.patch(f"/api/v1/companies/{cid}/status", json={"status": "investor_ready"})

    # Investisseur compatible
    good = client.post("/api/v1/investors", json={"name": "Good", "type": "equity_pe_vc"}).json()
    client.put(f"/api/v1/investors/{good['id']}/criteria", json=_criteria())
    # Investisseur incompatible (autre type de deal)
    bad = client.post("/api/v1/investors", json={"name": "Bad", "type": "banque"}).json()
    client.put(
        f"/api/v1/investors/{bad['id']}/criteria",
        json=_criteria(deal_types=["dette_bancaire"], instruments=["dette"]),
    )

    matches = client.get(f"/api/v1/companies/{cid}/matches").json()
    assert len(matches) == 1 and matches[0]["investor_name"] == "Good"
    assert matches[0]["passes_hard_filters"] is True
    assert matches[0]["fit_score"] > 0.5

    # avec non éligibles
    allm = client.get(
        f"/api/v1/companies/{cid}/matches", params={"include_non_eligible": "true"}
    ).json()
    assert len(allm) == 2
    bad_row = next(m for m in allm if m["investor_name"] == "Bad")
    assert bad_row["passes_hard_filters"] is False
    assert "Type de deal non couvert" in bad_row["reasons"]
    _clear()


def test_matching_domain_unit():
    company = {"country": "CI", "sector": "Agro", "instrument": "equity",
               "deal_type": "ouverture_capital", "amount": 80000000, "stage": None}
    crit = {"countries": ["CI"], "sectors": ["Agro"], "instruments": ["equity"],
            "deal_types": ["ouverture_capital"], "stages": [], "exclusions": [],
            "ticket_min": 10000000, "ticket_max": 200000000}
    passes, fit, _ = matching.evaluate(company, crit)
    assert passes is True and fit > 0.7

    crit_excl = {**crit, "exclusions": ["Agro"]}
    passes2, fit2, reasons2 = matching.evaluate(company, crit_excl)
    assert passes2 is False and fit2 == 0.0 and "Exclusion explicite" in reasons2
