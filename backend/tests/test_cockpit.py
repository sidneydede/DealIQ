"""Tests Lot 4 — cockpit (M20), reporting (M21), lecture audit (M22)."""
from app.api.deps import get_current_user
from app.core.security import hash_password
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


def _full_funnel(client, name="Acme", deal_type="ouverture_capital"):
    """Crée une entreprise, choisit un type, complète l'onboarding, demande un devis."""
    cid = client.post(
        "/api/v1/companies", json={"name": name, "country": "CI", "sector": "Agro"}
    ).json()["company"]["id"]
    client.post(
        f"/api/v1/companies/{cid}/deal-type",
        json={"deal_type_primary": deal_type, "amount": 80000000, "use_of_funds": "Croissance"},
    )
    client.put(
        f"/api/v1/companies/{cid}/questionnaire",
        json={"answers": {"amount": 80000000}, "current_step": 5},
    )
    client.post(f"/api/v1/companies/{cid}/questionnaire/consent", json={"consent_text": "OK ok"})
    client.post(f"/api/v1/companies/{cid}/questionnaire/submit")
    client.post(f"/api/v1/companies/{cid}/score")
    client.post(f"/api/v1/companies/{cid}/quote-request", json={"offer_key": "preparation"})
    return cid


def test_cockpit_requires_cabinet(client, db_session):
    _auth(_user(db_session, "e@dealiq.com"))
    assert client.get("/api/v1/cockpit/companies").status_code == 403
    _auth(_user(db_session, "a@dealiq.com", Role.analyste))
    assert client.get("/api/v1/cockpit/companies").status_code == 200
    _clear()


def test_cockpit_enriched_and_filters(client, db_session):
    _auth(_user(db_session, "e@dealiq.com"))
    _full_funnel(client, name="Equity Co", deal_type="ouverture_capital")
    _full_funnel(client, name="Dette Co", deal_type="dette_bancaire")

    _auth(_user(db_session, "a@dealiq.com", Role.analyste))
    payload = client.get("/api/v1/cockpit/companies").json()
    assert payload["total"] == 2
    items = payload["items"]
    assert len(items) == 2
    first = items[0]
    assert "readiness_category" in first and "quote_requests" in first
    assert first["quote_requests"] >= 1

    # filtre par type de deal
    only_dette = client.get(
        "/api/v1/cockpit/companies", params={"deal_type": "dette_bancaire"}
    ).json()
    assert only_dette["total"] == 1 and only_dette["items"][0]["name"] == "Dette Co"

    # recherche plein-texte (nom / secteur)
    search = client.get("/api/v1/cockpit/companies", params={"q": "equity"}).json()
    assert search["total"] == 1 and search["items"][0]["name"] == "Equity Co"

    # pagination
    paged = client.get("/api/v1/cockpit/companies", params={"limit": 1, "offset": 0}).json()
    assert paged["total"] == 2 and len(paged["items"]) == 1 and paged["limit"] == 1
    _clear()


def test_pipeline_counts(client, db_session):
    _auth(_user(db_session, "e@dealiq.com"))
    _full_funnel(client)
    _auth(_user(db_session, "a@dealiq.com", Role.analyste))
    counts = client.get("/api/v1/cockpit/pipeline").json()
    assert counts["brouillon"] == 1
    _clear()


def test_quote_status_update(client, db_session):
    _auth(_user(db_session, "e@dealiq.com"))
    cid = _full_funnel(client)
    _auth(_user(db_session, "s@dealiq.com", Role.senior))
    quotes = client.get(f"/api/v1/companies/{cid}/quote-requests").json()
    qid = quotes[0]["id"]
    r = client.patch(f"/api/v1/quote-requests/{qid}/status", json={"status": "traite"})
    assert r.status_code == 200 and r.json()["status"] == "traite"
    assert client.patch(
        f"/api/v1/quote-requests/{qid}/status", json={"status": "bidon"}
    ).status_code == 422
    _clear()


def test_reporting_dashboard(client, db_session):
    _auth(_user(db_session, "e@dealiq.com"))
    _full_funnel(client, name="Co1")
    _auth(_user(db_session, "a@dealiq.com", Role.analyste))
    d = client.get("/api/v1/reporting/dashboard").json()
    assert d["companies_total"] == 1
    assert d["onboarding_completed"] == 1
    assert d["completion_rate"] == 1.0
    assert d["quote_requests_total"] == 1
    assert d["by_deal_type"].get("ouverture_capital") == 1
    assert "investor_ready" in d["by_readiness_category"] or len(d["by_readiness_category"]) >= 1
    _clear()


def test_audit_read_admin_only(client, db_session):
    _auth(_user(db_session, "e@dealiq.com"))
    _full_funnel(client)
    # non-admin (analyste) interdit
    _auth(_user(db_session, "a@dealiq.com", Role.analyste))
    assert client.get("/api/v1/audit").status_code == 403
    # admin autorisé
    _auth(_user(db_session, "admin@dealiq.com", Role.admin))
    payload = client.get("/api/v1/audit").json()
    assert payload["total"] > 0 and len(payload["items"]) > 0
    # filtre par action
    created = client.get("/api/v1/audit", params={"action": "company_created"}).json()
    assert all(log["action"] == "company_created" for log in created["items"])
    _clear()
