"""Tests M18 — DD OHADA/SYSCOHADA."""
from app.api.deps import get_current_user
from app.core.security import hash_password
from app.domain import syscohada
from app.domain.enums import AuditAction, DealTypeCode, Role
from app.main import app
from app.models.audit import AuditLog
from app.models.user import User

BALANCE = [
    {"account": "701000", "label": "Ventes", "amount": 1000000},
    {"account": "601000", "label": "Achats", "amount": 400000},
    {"account": "681000", "label": "Dotations", "amount": 100000},
    {"account": "164000", "label": "Emprunts", "amount": 300000},
    {"account": "521000", "label": "Banque", "amount": 50000},
    {"account": "311000", "label": "Stocks", "amount": 200000},
    {"account": "411000", "label": "Clients", "amount": 150000},
    {"account": "401000", "label": "Fournisseurs", "amount": 120000},
]


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


def _company(client, deal_type="dette_bancaire"):
    cid = client.post(
        "/api/v1/companies", json={"name": "Acme", "country": "CI", "sector": "Agro"}
    ).json()["company"]["id"]
    client.post(f"/api/v1/companies/{cid}/deal-type", json={"deal_type_primary": deal_type})
    return cid


# --- domaine pur ---
def test_retraitements_pure():
    r = syscohada.retraitements(BALANCE)
    assert r["chiffre_affaires"]["value"] == 1000000
    assert r["ebitda"]["value"] == 600000  # 1,000,000 - 400,000
    assert r["dette_nette"]["value"] == 250000  # 300,000 - 50,000
    assert r["bfr"]["value"] == 230000  # 200,000 + 150,000 - 120,000
    # traçabilité : règle + sources présentes (RG-M18-02)
    assert r["ebitda"]["rule"] and r["ebitda"]["sources"]
    # focus adapté au type de deal (RG-M18-03)
    assert any("remboursement" in f for f in syscohada.dd_focus(DealTypeCode.dette_bancaire))
    assert any("Valorisation" in f for f in syscohada.dd_focus(DealTypeCode.ouverture_capital))


# --- API ---
def test_import_requires_cabinet(client, db_session):
    _auth(_user(db_session, "e@dealiq.com"))
    cid = _company(client)
    r = client.post(f"/api/v1/companies/{cid}/syscohada", json={"lines": BALANCE})
    assert r.status_code == 403
    _clear()


def test_import_versioning_and_compute(client, db_session):
    _auth(_user(db_session, "e@dealiq.com"))
    cid = _company(client, deal_type="dette_bancaire")

    _auth(_user(db_session, "a@dealiq.com", Role.analyste))
    # compute sans balance -> 409
    assert client.post(f"/api/v1/companies/{cid}/dd/compute").status_code == 409

    v1 = client.post(
        f"/api/v1/companies/{cid}/syscohada", json={"lines": BALANCE, "fiscal_year": "2024"}
    )
    assert v1.status_code == 201 and v1.json()["version"] == 1
    v2 = client.post(f"/api/v1/companies/{cid}/syscohada", json={"lines": BALANCE})
    assert v2.json()["version"] == 2

    dd = client.post(f"/api/v1/companies/{cid}/dd/compute").json()
    assert dd["retraitements"]["ebitda"]["value"] == 600000
    assert dd["deal_type"] == "dette_bancaire"
    assert any("remboursement" in f for f in dd["focus"])  # axes DD crédit
    assert "EBITDA" in dd["synthesis"]
    assert dd["class_totals"]["7"] == 1000000
    assert (
        db_session.query(AuditLog).filter(AuditLog.action == AuditAction.dd_computed).count() == 1
    )

    # récupération de la dernière analyse
    got = client.get(f"/api/v1/companies/{cid}/dd").json()
    assert got["retraitements"]["bfr"]["value"] == 230000
    _clear()


def test_focus_equity(client, db_session):
    _auth(_user(db_session, "e@dealiq.com"))
    cid = _company(client, deal_type="ouverture_capital")
    _auth(_user(db_session, "a@dealiq.com", Role.analyste))
    client.post(f"/api/v1/companies/{cid}/syscohada", json={"lines": BALANCE})
    dd = client.post(f"/api/v1/companies/{cid}/dd/compute").json()
    assert any("Valorisation" in f for f in dd["focus"])
    _clear()
