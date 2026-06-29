"""Tests M8 — espace mission / préparation."""
from app.api.deps import get_current_user
from app.core.security import hash_password
from app.domain.enums import AuditAction, Role
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


def _company(client, db_session):
    entr = _user(db_session, "e@dealiq.com")
    _auth(entr)
    cid = client.post(
        "/api/v1/companies", json={"name": "Acme", "country": "CI", "sector": "Agro"}
    ).json()["company"]["id"]
    client.post(
        f"/api/v1/companies/{cid}/deal-type", json={"deal_type_primary": "ouverture_capital"}
    )
    return cid, entr


def _mission(client, db_session, cid):
    _auth(_user(db_session, "a@dealiq.com", Role.analyste))
    return client.post(f"/api/v1/companies/{cid}/mission").json()


def test_mission_seeds_checklist_by_type(client, db_session):
    cid, _ = _company(client, db_session)
    m = _mission(client, db_session, cid)
    labels = [t["label"] for t in m["tasks"]]
    assert "Business plan validé" in labels
    assert "Cap table à jour" in labels  # spécifique equity
    assert m["can_promote"] is False
    _clear()


def test_entrepreneur_can_read_mission(client, db_session):
    cid, entr = _company(client, db_session)
    _mission(client, db_session, cid)
    _auth(entr)
    r = client.get(f"/api/v1/companies/{cid}/mission")
    assert r.status_code == 200
    # mais ne peut pas modifier une tâche
    tid = r.json()["tasks"][0]["id"]
    assert client.patch(f"/api/v1/mission-tasks/{tid}", json={"done": True}).status_code == 403
    _clear()


def test_deliverable_versioning(client, db_session):
    cid, _ = _company(client, db_session)
    m = _mission(client, db_session, cid)
    mid = m["id"]
    _auth(_user(db_session, "a@dealiq.com", Role.analyste))
    v1 = client.post(f"/api/v1/missions/{mid}/deliverables", json={"kind": "business_plan"})
    assert v1.json()["version"] == 1
    v2 = client.post(f"/api/v1/missions/{mid}/deliverables", json={"kind": "business_plan"})
    assert v2.json()["version"] == 2
    upd = client.patch(f"/api/v1/deliverables/{v2.json()['id']}", json={"status": "valide"})
    assert upd.json()["status"] == "valide"
    _clear()


def _complete_checklist(client, mission):
    for t in mission["tasks"]:
        client.patch(f"/api/v1/mission-tasks/{t['id']}", json={"done": True})


def test_promote_requires_checklist_and_double_validation(client, db_session):
    cid, _ = _company(client, db_session)
    m = _mission(client, db_session, cid)
    mid = m["id"]

    # tout coché mais sans validation → 409
    _auth(_user(db_session, "a@dealiq.com", Role.analyste))
    _complete_checklist(client, m)
    r = client.post(f"/api/v1/missions/{mid}/promote")
    assert r.status_code == 409 and "Validation senior" in r.json()["detail"]

    # validation analyste puis senior
    client.post(f"/api/v1/missions/{mid}/review")  # analyste (auth courant)
    _auth(_user(db_session, "s@dealiq.com", Role.senior))
    client.post(f"/api/v1/missions/{mid}/review")  # senior

    # promotion → investor-ready
    r = client.post(f"/api/v1/missions/{mid}/promote")
    assert r.status_code == 200 and r.json()["status"] == "investor_ready"
    assert (
        db_session.query(AuditLog)
        .filter(AuditLog.action == AuditAction.mission_promoted)
        .count()
        == 1
    )
    _clear()
