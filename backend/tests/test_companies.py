"""Tests Lot 1 — M2 (entreprise) et M24 (type de deal)."""
from app.api.deps import get_current_user
from app.core.security import hash_password
from app.domain.enums import AuditAction, Role
from app.main import app
from app.models.audit import AuditLog
from app.models.user import User


def _mk_user(db, email, role=Role.entrepreneur) -> User:
    u = User(email=email, hashed_password=hash_password("x"), role=role)
    db.add(u)
    db.commit()
    db.refresh(u)
    return u


def _auth_as(user: User):
    app.dependency_overrides[get_current_user] = lambda: user


def _create_company(client, **over):
    body = {"name": "Acme SARL", "country": "CI", "sector": "Agro"}
    body.update(over)
    return client.post("/api/v1/companies", json=body)


def test_company_update_is_historized(client, db_session):
    entr = _mk_user(db_session, "hist@dealiq.com")
    _auth_as(entr)
    cid = _create_company(client, name="Acme SARL", sector="Agro").json()["company"]["id"]

    r = client.patch(f"/api/v1/companies/{cid}", json={"name": "Acme Group", "sector": "Tech"})
    assert r.status_code == 200 and r.json()["name"] == "Acme Group"

    hist = client.get(f"/api/v1/companies/{cid}/history").json()
    by_field = {h["field"]: h for h in hist}
    assert by_field["name"]["old_value"] == "Acme SARL"
    assert by_field["name"]["new_value"] == "Acme Group"
    assert by_field["sector"]["old_value"] == "Agro"
    assert by_field["sector"]["new_value"] == "Tech"
    assert all(h["changed_by"] == entr.id for h in hist)

    # Une PATCH sans changement réel n'ajoute pas d'entrée.
    client.patch(f"/api/v1/companies/{cid}", json={"name": "Acme Group"})
    assert len(client.get(f"/api/v1/companies/{cid}/history").json()) == 2
    app.dependency_overrides.pop(get_current_user, None)


def test_create_company_defaults(client, db_session):
    entr = _mk_user(db_session, "a@dealiq.com")
    _auth_as(entr)
    r = _create_company(client)
    assert r.status_code == 201
    company = r.json()["company"]
    assert company["currency"] == "XOF"  # CI -> UEMOA
    assert company["financials_reliability"] == "declare_non_audite"
    assert company["status"] == "brouillon"
    assert company["owner_id"] == entr.id
    assert r.json()["duplicate_warnings"] == []
    app.dependency_overrides.pop(get_current_user, None)


def test_duplicate_is_flagged_not_blocked(client, db_session):
    _auth_as(_mk_user(db_session, "a@dealiq.com"))
    assert _create_company(client).status_code == 201
    r = _create_company(client, name="acme  sarl")  # même nom normalisé + pays
    assert r.status_code == 201
    warns = r.json()["duplicate_warnings"]
    assert len(warns) == 1 and warns[0]["reason"] == "name"
    app.dependency_overrides.pop(get_current_user, None)


def test_listing_is_scoped_by_role(client, db_session):
    entr_a = _mk_user(db_session, "a@dealiq.com")
    entr_b = _mk_user(db_session, "b@dealiq.com")
    _auth_as(entr_a)
    _create_company(client, name="A Co")
    _auth_as(entr_b)
    _create_company(client, name="B Co")

    # chaque entrepreneur ne voit que sa fiche
    assert len(client.get("/api/v1/companies").json()) == 1
    # le cabinet voit tout
    _auth_as(_mk_user(db_session, "analyste2@dealiq.com", Role.analyste))
    assert len(client.get("/api/v1/companies").json()) == 2
    app.dependency_overrides.pop(get_current_user, None)


def test_entrepreneur_cannot_access_other_company(client, db_session):
    entr_a = _mk_user(db_session, "a@dealiq.com")
    _auth_as(entr_a)
    cid = _create_company(client).json()["company"]["id"]
    _auth_as(_mk_user(db_session, "b@dealiq.com"))
    assert client.get(f"/api/v1/companies/{cid}").status_code == 403
    app.dependency_overrides.pop(get_current_user, None)


def test_status_change_requires_cabinet_and_is_audited(client, db_session):
    entr = _mk_user(db_session, "a@dealiq.com")
    _auth_as(entr)
    cid = _create_company(client).json()["company"]["id"]
    # entrepreneur interdit
    r = client.patch(f"/api/v1/companies/{cid}/status", json={"status": "qualifie"})
    assert r.status_code == 403
    # cabinet autorisé
    _auth_as(_mk_user(db_session, "senior@dealiq.com", Role.senior))
    r = client.patch(f"/api/v1/companies/{cid}/status", json={"status": "qualifie"})
    assert r.status_code == 200 and r.json()["status"] == "qualifie"
    assert (
        db_session.query(AuditLog)
        .filter(AuditLog.action == AuditAction.company_status_changed)
        .count()
        == 1
    )
    app.dependency_overrides.pop(get_current_user, None)


def test_deal_type_selection_and_history(client, db_session):
    entr = _mk_user(db_session, "a@dealiq.com")
    _auth_as(entr)
    cid = _create_company(client).json()["company"]["id"]

    r = client.post(
        f"/api/v1/companies/{cid}/deal-type",
        json={"deal_type_primary": "ouverture_capital", "amount": 50000000},
    )
    assert r.status_code == 200
    assert r.json()["deal_type_primary"] == "ouverture_capital"

    hist = client.get(f"/api/v1/companies/{cid}/deal-type/history").json()
    assert len(hist) == 1
    assert hist[0]["source"] == "entrepreneur"
    assert hist[0]["new_primary"] == "ouverture_capital"
    app.dependency_overrides.pop(get_current_user, None)


def test_secondary_must_differ_from_primary(client, db_session):
    _auth_as(_mk_user(db_session, "a@dealiq.com"))
    cid = _create_company(client).json()["company"]["id"]
    r = client.post(
        f"/api/v1/companies/{cid}/deal-type",
        json={"deal_type_primary": "dette_bancaire", "deal_type_secondary": "dette_bancaire"},
    )
    assert r.status_code == 422
    app.dependency_overrides.pop(get_current_user, None)


def test_requalification_is_cabinet_only(client, db_session):
    entr = _mk_user(db_session, "a@dealiq.com")
    _auth_as(entr)
    cid = _create_company(client).json()["company"]["id"]
    client.post(
        f"/api/v1/companies/{cid}/deal-type", json={"deal_type_primary": "ouverture_capital"}
    )

    # entrepreneur ne peut pas requalifier
    r = client.post(
        f"/api/v1/companies/{cid}/deal-type/requalify",
        json={"deal_type_primary": "dette_bancaire", "motif": "Cash-flow adapté à la dette"},
    )
    assert r.status_code == 403

    # cabinet requalifie, motif enregistré, historique à 2 entrées
    _auth_as(_mk_user(db_session, "senior@dealiq.com", Role.senior))
    r = client.post(
        f"/api/v1/companies/{cid}/deal-type/requalify",
        json={"deal_type_primary": "dette_bancaire", "motif": "Cash-flow adapté à la dette"},
    )
    assert r.status_code == 200 and r.json()["deal_type_primary"] == "dette_bancaire"
    hist = client.get(f"/api/v1/companies/{cid}/deal-type/history").json()
    assert len(hist) == 2
    sources = [h["source"] for h in hist]
    assert sources.count("entrepreneur") == 1 and sources.count("cabinet") == 1
    cabinet_entry = next(h for h in hist if h["source"] == "cabinet")
    assert cabinet_entry["motif"].startswith("Cash-flow")
    assert cabinet_entry["old_primary"] == "ouverture_capital"
    assert cabinet_entry["new_primary"] == "dette_bancaire"
    app.dependency_overrides.pop(get_current_user, None)


def test_requalify_requires_motif(client, db_session):
    _auth_as(_mk_user(db_session, "senior@dealiq.com", Role.senior))
    cid = _create_company(client).json()["company"]["id"]
    r = client.post(
        f"/api/v1/companies/{cid}/deal-type/requalify",
        json={"deal_type_primary": "dette_bancaire"},
    )
    assert r.status_code == 422
    app.dependency_overrides.pop(get_current_user, None)
