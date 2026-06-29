"""Tests calibrage scoring — config paramétrable + simulateur."""
from app.api.deps import get_current_user
from app.core.security import hash_password
from app.domain import scoring
from app.domain.enums import CompanyStage, ReadinessCategory, Role
from app.main import app
from app.models.user import User

SIGNALS = {
    "traction": 0.6, "profitabilite_cashflow": 0.6, "qualite_info_financiere": 0.6,
    "clarte_besoin": 0.6, "gouvernance": 0.6, "qualite_documentaire": 0.6,
    "scalabilite_marche": 0.6, "esg": 0.6,
}


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


# --- domaine : seuils paramétrables ---
def test_map_category_with_custom_thresholds():
    # 60/100, pièces vérifiées, non-early
    base = dict(stage=None, deal_type=None, has_verified_financials=True)
    assert scoring.map_category(60, **base) == ReadinessCategory.a_preparer  # seuil défaut 70
    assert (
        scoring.map_category(60, **base, thresholds={"investor_ready_min": 50})
        == ReadinessCategory.investor_ready
    )
    # early + seuil précoce
    assert (
        scoring.map_category(40, stage=CompanyStage.amorcage, deal_type=None,
                             has_verified_financials=True)
        == ReadinessCategory.trop_precoce
    )


# --- config admin ---
def test_config_rbac_and_update(client, db_session):
    _auth(_user(db_session, "e@dealiq.com"))
    assert client.get("/api/v1/admin/scoring/config").status_code == 403
    _auth(_user(db_session, "a@dealiq.com", Role.analyste))
    assert client.get("/api/v1/admin/scoring/config").status_code == 403

    _auth(_user(db_session, "admin@dealiq.com", Role.admin))
    cfg = client.get("/api/v1/admin/scoring/config").json()
    assert cfg["thresholds"]["investor_ready_min"] == 70.0
    assert "ouverture_capital" in cfg["deal_type_weights"]  # depuis le référentiel

    upd = client.put(
        "/api/v1/admin/scoring/config",
        json={"thresholds": {"investor_ready_min": 60.0, "early_precoce_max": 45.0,
                             "precoce_floor": 30.0}, "version": "calibrage-2026"},
    )
    assert upd.status_code == 200
    assert upd.json()["thresholds"]["investor_ready_min"] == 60.0
    assert upd.json()["version"] == "calibrage-2026"
    _clear()


# --- simulateur ---
def test_simulate_direct_signals_and_override(client, db_session):
    _auth(_user(db_session, "a@dealiq.com", Role.analyste))
    body = {"signals": SIGNALS, "has_verified_financials": True}
    r = client.post("/api/v1/admin/scoring/simulate", json=body)
    assert r.status_code == 200
    assert r.json()["total"] == 60.0
    assert r.json()["category"] == "a_preparer"  # seuil défaut 70

    # override : abaisser le seuil → investor-ready (effet de calibrage visible)
    body2 = {**body, "config_override": {"thresholds": {"investor_ready_min": 50}}}
    sim = client.post("/api/v1/admin/scoring/simulate", json=body2).json()
    assert sim["category"] == "investor_ready"
    _clear()


def test_simulate_requires_cabinet(client, db_session):
    _auth(_user(db_session, "e@dealiq.com"))
    r = client.post("/api/v1/admin/scoring/simulate", json={"signals": SIGNALS})
    assert r.status_code == 403
    _clear()


def test_simulate_by_company(client, db_session):
    _auth(_user(db_session, "e@dealiq.com"))
    cid = client.post(
        "/api/v1/companies", json={"name": "Acme", "country": "CI", "sector": "Agro"}
    ).json()["company"]["id"]
    client.post(
        f"/api/v1/companies/{cid}/deal-type", json={"deal_type_primary": "ouverture_capital"}
    )

    _auth(_user(db_session, "a@dealiq.com", Role.analyste))
    r = client.post("/api/v1/admin/scoring/simulate", json={"company_id": cid})
    assert r.status_code == 200 and r.json()["category"] is not None
    _clear()
