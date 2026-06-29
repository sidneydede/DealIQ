"""Tests tâches & relances CRM (M20, US-M20-02)."""
from __future__ import annotations

from datetime import UTC, datetime, timedelta

from app.api.deps import get_current_user
from app.core.security import hash_password
from app.domain.enums import Role
from app.main import app
from app.models.user import User


def _as(db, role=Role.analyste):
    u = User(email=f"{role.value}-task@dealiq.com", hashed_password=hash_password("x"), role=role)
    db.add(u)
    db.commit()
    db.refresh(u)
    app.dependency_overrides[get_current_user] = lambda: u
    return u


def _clear():
    app.dependency_overrides.pop(get_current_user, None)


def test_task_crud_and_done(client, db_session):
    _as(db_session, Role.analyste)
    created = client.post("/api/v1/tasks", json={"title": "Relancer Sahel Capital"})
    assert created.status_code == 201
    tid = created.json()["id"]
    assert created.json()["status"] == "a_faire" and created.json()["overdue"] is False

    assert len(client.get("/api/v1/tasks").json()) == 1

    done = client.patch(f"/api/v1/tasks/{tid}", json={"status": "fait"})
    assert done.status_code == 200 and done.json()["status"] == "fait"

    # filtre par statut
    assert len(client.get("/api/v1/tasks", params={"status_filter": "a_faire"}).json()) == 0
    assert len(client.get("/api/v1/tasks", params={"status_filter": "fait"}).json()) == 1

    assert client.delete(f"/api/v1/tasks/{tid}").status_code == 200
    assert len(client.get("/api/v1/tasks").json()) == 0
    _clear()


def test_overdue_relance_flag(client, db_session):
    _as(db_session, Role.senior)
    past = (datetime.now(UTC) - timedelta(days=1)).isoformat()
    future = (datetime.now(UTC) + timedelta(days=3)).isoformat()
    client.post("/api/v1/tasks", json={"title": "En retard", "due_date": past})
    client.post("/api/v1/tasks", json={"title": "À venir", "due_date": future})

    overdue = client.get("/api/v1/tasks", params={"overdue": "true"}).json()
    assert len(overdue) == 1 and overdue[0]["title"] == "En retard"
    assert overdue[0]["overdue"] is True
    _clear()


def test_tasks_require_cabinet(client, db_session):
    _as(db_session, Role.entrepreneur)
    assert client.get("/api/v1/tasks").status_code == 403
    assert client.post("/api/v1/tasks", json={"title": "x"}).status_code == 403
    _clear()
