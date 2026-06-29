"""Tests M16 — pipeline deal execution."""
from app.api.deps import get_current_user
from app.core.security import hash_password
from app.domain import deal as dealdom
from app.domain.enums import AuditAction, DealStage, DealTypeCode, Role
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


def _interaction(client, db_session, deal_type="ouverture_capital", nda=False):
    _auth(_user(db_session, "e@dealiq.com"))
    cid = client.post(
        "/api/v1/companies", json={"name": "Acme", "country": "CI", "sector": "Agro"}
    ).json()["company"]["id"]
    client.post(
        f"/api/v1/companies/{cid}/deal-type",
        json={"deal_type_primary": deal_type, "amount": 80000000},
    )
    client.post(f"/api/v1/companies/{cid}/score")

    fund = _user(db_session, "fund@dealiq.com", Role.investisseur)
    _auth(_user(db_session, "a@dealiq.com", Role.analyste))
    client.patch(f"/api/v1/companies/{cid}/status", json={"status": "investor_ready"})
    tid = client.post(f"/api/v1/companies/{cid}/teaser").json()["id"]
    client.post(f"/api/v1/teasers/{tid}/publish")
    client.post(
        "/api/v1/investors",
        json={"name": "Fund", "type": "equity_pe_vc", "user_email": "fund@dealiq.com"},
    )
    _auth(fund)
    iid = client.post(f"/api/v1/teasers/{tid}/interest", json={}).json()["id"]
    if nda:
        _auth(_user(db_session, "a@dealiq.com", Role.analyste))
        client.patch(f"/api/v1/interactions/{iid}/status", json={"status": "nda_signe"})
    return cid, iid


def _cabinet(db_session):
    _auth(_user(db_session, "a@dealiq.com", Role.analyste))


# --- domaine pur ---
def test_domain_milestones_and_next():
    eq = dealdom.milestones_for(DealTypeCode.ouverture_capital)
    assert any("SHA" in m for m in eq)
    dette = dealdom.milestones_for(DealTypeCode.dette_bancaire)
    assert any("Convention de crédit" in m for m in dette)
    assert dealdom.next_stage(DealStage.interesse) == DealStage.nda
    assert dealdom.next_stage(DealStage.closing) is None


# --- création ---
def test_create_deal_initializes_milestones(client, db_session):
    _, iid = _interaction(client, db_session)
    _cabinet(db_session)
    r = client.post(f"/api/v1/interactions/{iid}/deal")
    assert r.status_code == 201
    deal = r.json()
    assert deal["deal_type"] == "ouverture_capital" and deal["stage"] == "interesse"
    did = deal["id"]

    # idempotent
    assert client.post(f"/api/v1/interactions/{iid}/deal").json()["id"] == did

    detail = client.get(f"/api/v1/deals/{did}").json()
    assert any("SHA" in m["label"] for m in detail["milestones"])
    assert len(detail["history"]) == 1
    assert (
        db_session.query(AuditLog).filter(AuditLog.action == AuditAction.deal_created).count() == 1
    )
    _clear()


def test_stage_derived_from_nda(client, db_session):
    _, iid = _interaction(client, db_session, nda=True)
    _cabinet(db_session)
    deal = client.post(f"/api/v1/interactions/{iid}/deal").json()
    assert deal["stage"] == "data_room"  # NDA signé → data room
    _clear()


def test_advance_stage_traced(client, db_session):
    _, iid = _interaction(client, db_session)
    _cabinet(db_session)
    did = client.post(f"/api/v1/interactions/{iid}/deal").json()["id"]
    r = client.patch(
        f"/api/v1/deals/{did}/stage", json={"stage": "due_diligence", "note": "DD lancée"}
    )
    assert r.status_code == 200 and r.json()["stage"] == "due_diligence"
    detail = client.get(f"/api/v1/deals/{did}").json()
    assert len(detail["history"]) == 2
    assert (
        db_session.query(AuditLog)
        .filter(AuditLog.action == AuditAction.deal_stage_changed)
        .count()
        == 1
    )
    _clear()


def test_toggle_milestone(client, db_session):
    _, iid = _interaction(client, db_session)
    _cabinet(db_session)
    did = client.post(f"/api/v1/interactions/{iid}/deal").json()["id"]
    mid = client.get(f"/api/v1/deals/{did}").json()["milestones"][0]["id"]
    r = client.patch(f"/api/v1/deal-milestones/{mid}", json={"done": True})
    assert r.status_code == 200 and r.json()["done"] is True
    _clear()


def test_pipeline_filters_and_rbac(client, db_session):
    _, iid = _interaction(client, db_session)
    _cabinet(db_session)
    client.post(f"/api/v1/interactions/{iid}/deal")
    assert client.get("/api/v1/deals").json()["total"] == 1
    assert client.get("/api/v1/deals", params={"stage": "closing"}).json()["total"] == 0

    # entrepreneur interdit
    _auth(_user(db_session, "e@dealiq.com"))
    assert client.get("/api/v1/deals").status_code == 403
    _clear()


def test_dashboard_investor_funnel(client, db_session):
    # _interaction crée : entreprise, investisseur, teaser publié, interaction (intérêt).
    _interaction(client, db_session)
    _cabinet(db_session)
    d = client.get("/api/v1/reporting/dashboard").json()
    assert d["investors_total"] >= 1
    assert d["teasers_published"] >= 1
    assert d["interactions_total"] >= 1
    assert d["interactions_by_status"].get("interesse", 0) >= 1
    assert "interest_to_deal_rate" in d and "deals_closing" in d
    _clear()


def test_deals_csv_export(client, db_session):
    _, iid = _interaction(client, db_session)
    _cabinet(db_session)
    client.post(f"/api/v1/interactions/{iid}/deal")

    r = client.get("/api/v1/deals.csv")
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("text/csv")
    assert "attachment" in r.headers["content-disposition"]
    assert r.text.startswith("﻿")
    assert "Entreprise;Investisseur;Type de deal" in r.text
    assert "Acme" in r.text and "Fund" in r.text

    # entrepreneur interdit
    _auth(_user(db_session, "e@dealiq.com"))
    assert client.get("/api/v1/deals.csv").status_code == 403
    _clear()


def test_dashboard_includes_deals(client, db_session):
    _, iid = _interaction(client, db_session)
    _cabinet(db_session)
    client.post(f"/api/v1/interactions/{iid}/deal")
    d = client.get("/api/v1/reporting/dashboard").json()
    assert d["deals_total"] == 1
    assert d["deals_by_stage"].get("interesse") == 1
    _clear()
