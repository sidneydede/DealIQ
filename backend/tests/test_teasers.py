"""Tests V1-B — M11 (teaser/anonymisation) et M12 (intérêt/mise en relation)."""
from app.api.deps import get_current_user
from app.core.security import hash_password
from app.domain import teaser as anon
from app.domain.enums import AuditAction, DealTypeCode, Role, Zone
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


def _ready_company(client, name="Secret Corp"):
    cid = client.post(
        "/api/v1/companies", json={"name": name, "country": "CI", "sector": "Agro"}
    ).json()["company"]["id"]
    client.post(
        f"/api/v1/companies/{cid}/deal-type",
        json={"deal_type_primary": "ouverture_capital", "amount": 80000000},
    )
    client.post(f"/api/v1/companies/{cid}/score")
    return cid


# --- domaine pur ---
def test_anonymization_helpers():
    assert anon.band(None) == "Non communiqué"
    assert anon.band(30_000_000) == "< 50 M FCFA"
    assert anon.band(80_000_000) == "50 – 200 M FCFA"
    assert anon.band(5_000_000_000) == "> 1 Md FCFA"
    title = anon.build_title("Agro", Zone.UEMOA, DealTypeCode.ouverture_capital)
    assert "Agro" in title and "UEMOA" in title


# --- M11 ---
def test_generate_requires_investor_ready(client, db_session):
    _auth(_user(db_session, "e@dealiq.com"))
    cid = _ready_company(client)
    _auth(_user(db_session, "a@dealiq.com", Role.analyste))
    assert client.post(f"/api/v1/companies/{cid}/teaser").status_code == 409
    _clear()


def test_teaser_is_anonymized_and_publishable(client, db_session):
    _auth(_user(db_session, "e@dealiq.com"))
    cid = _ready_company(client, name="Secret Corp")
    cab = _user(db_session, "a@dealiq.com", Role.analyste)
    _auth(cab)
    client.patch(f"/api/v1/companies/{cid}/status", json={"status": "investor_ready"})

    t = client.post(f"/api/v1/companies/{cid}/teaser").json()
    assert t["status"] == "brouillon"
    assert "Secret" not in t["title"]  # pas de nom (RG-M11-01)
    assert t["zone"] == "UEMOA"
    assert t["instrument"] == "equity"

    pub = client.post(f"/api/v1/teasers/{t['id']}/publish").json()
    assert pub["status"] == "publie"
    assert (
        db_session.query(AuditLog)
        .filter(AuditLog.action == AuditAction.teaser_published)
        .count()
        == 1
    )
    _clear()


def test_investor_catalog_is_anonymized(client, db_session):
    _auth(_user(db_session, "e@dealiq.com"))
    cid = _ready_company(client, name="Secret Corp")
    cab = _user(db_session, "a@dealiq.com", Role.analyste)
    _auth(cab)
    client.patch(f"/api/v1/companies/{cid}/status", json={"status": "investor_ready"})
    tid = client.post(f"/api/v1/companies/{cid}/teaser").json()["id"]
    client.post(f"/api/v1/teasers/{tid}/publish")

    _auth(_user(db_session, "inv@dealiq.com", Role.investisseur))
    catalog = client.get("/api/v1/teasers").json()
    assert len(catalog) == 1
    # vue investisseur : aucun champ ré-identifiant
    assert "company_id" not in catalog[0]
    assert "Secret" not in catalog[0]["title"]
    # filtre
    assert len(client.get("/api/v1/teasers", params={"instrument": "equity"}).json()) == 1
    assert len(client.get("/api/v1/teasers", params={"instrument": "dette"}).json()) == 0
    _clear()


# --- M12 ---
def _published_teaser(client, db_session):
    _auth(_user(db_session, "e@dealiq.com"))
    cid = _ready_company(client)
    cab = _user(db_session, "a@dealiq.com", Role.analyste)
    _auth(cab)
    client.patch(f"/api/v1/companies/{cid}/status", json={"status": "investor_ready"})
    tid = client.post(f"/api/v1/companies/{cid}/teaser").json()["id"]
    client.post(f"/api/v1/teasers/{tid}/publish")
    return tid


def test_interest_requires_investor_fiche(client, db_session):
    tid = _published_teaser(client, db_session)
    # entrepreneur ne peut pas
    _auth(_user(db_session, "e2@dealiq.com"))
    assert client.post(f"/api/v1/teasers/{tid}/interest", json={}).status_code == 403
    # investisseur sans fiche -> 400
    _auth(_user(db_session, "inv@dealiq.com", Role.investisseur))
    assert client.post(f"/api/v1/teasers/{tid}/interest", json={}).status_code == 400
    _clear()


def test_full_interest_flow(client, db_session):
    tid = _published_teaser(client, db_session)
    inv_user = _user(db_session, "fund@dealiq.com", Role.investisseur)

    # cabinet crée la fiche investisseur liée au compte
    _auth(_user(db_session, "a3@dealiq.com", Role.analyste))
    client.post(
        "/api/v1/investors",
        json={"name": "Sahel Capital", "type": "equity_pe_vc", "user_email": "fund@dealiq.com"},
    )

    # l'investisseur manifeste son intérêt
    _auth(inv_user)
    r = client.post(f"/api/v1/teasers/{tid}/interest", json={"note": "Intéressé"})
    assert r.status_code == 201 and r.json()["status"] == "interesse"
    iid = r.json()["id"]
    # idempotent : 2e fois renvoie la même interaction
    assert client.post(f"/api/v1/teasers/{tid}/interest", json={}).json()["id"] == iid

    # cabinet voit l'intérêt et fait avancer le statut
    _auth(_user(db_session, "s@dealiq.com", Role.senior))
    interactions = client.get("/api/v1/interactions").json()
    assert len(interactions) == 1
    upd = client.patch(
        f"/api/v1/interactions/{iid}/status", json={"status": "nda_envoye"}
    )
    assert upd.status_code == 200 and upd.json()["status"] == "nda_envoye"
    assert (
        db_session.query(AuditLog)
        .filter(AuditLog.action == AuditAction.interaction_status_changed)
        .count()
        == 1
    )
    _clear()
