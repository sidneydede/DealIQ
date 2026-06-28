from app.domain.enums import AuditAction, Role
from app.models.audit import AuditLog
from app.models.user import User


def test_list_users_requires_admin(client, as_role):
    as_role(Role.entrepreneur)
    assert client.get("/api/v1/users").status_code == 403

    as_role(Role.admin)
    assert client.get("/api/v1/users").status_code == 200


def test_change_role_is_audited(client, db_session, as_role):
    admin = as_role(Role.admin)
    target = User(email="t@dealiq.com", hashed_password="x", role=Role.entrepreneur)
    db_session.add(target)
    db_session.commit()
    db_session.refresh(target)

    r = client.patch(f"/api/v1/users/{target.id}/role", json={"role": "analyste"})
    assert r.status_code == 200
    assert r.json()["role"] == "analyste"

    log = (
        db_session.query(AuditLog)
        .filter(AuditLog.action == AuditAction.role_changed)
        .one()
    )
    assert log.actor_id == admin.id
    assert log.meta == {"old": "entrepreneur", "new": "analyste"}


def test_login_failure_is_audited(client, db_session):
    client.post("/api/v1/auth/register", json={"email": "z@dealiq.com", "password": "Password123!"})
    client.post("/api/v1/auth/login", json={"email": "z@dealiq.com", "password": "bad"})
    failures = (
        db_session.query(AuditLog).filter(AuditLog.action == AuditAction.login_failed).all()
    )
    assert len(failures) == 1
    assert failures[0].actor_email == "z@dealiq.com"
