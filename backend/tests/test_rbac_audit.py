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


def test_admin_creates_user_with_generated_password(client, db_session, as_role):
    admin = as_role(Role.admin)
    r = client.post(
        "/api/v1/users",
        json={"email": "new@dealiq.com", "full_name": "Nouveau", "role": "analyste"},
    )
    assert r.status_code == 201
    body = r.json()
    assert body["email"] == "new@dealiq.com"
    assert body["role"] == "analyste"
    assert body["is_active"] is True
    # Mot de passe temporaire renvoyé une seule fois car non fourni.
    assert body["temporary_password"]

    created = db_session.query(User).filter(User.email == "new@dealiq.com").one()
    log = (
        db_session.query(AuditLog)
        .filter(AuditLog.action == AuditAction.user_created, AuditLog.object_id == created.id)
        .one()
    )
    assert log.actor_id == admin.id
    assert log.meta == {"role": "analyste", "by_admin": True}


def test_create_user_with_explicit_password_can_login(client, as_role):
    as_role(Role.admin)
    r = client.post(
        "/api/v1/users",
        json={"email": "boss@dealiq.com", "role": "senior", "password": "Password123!"},
    )
    assert r.status_code == 201
    assert r.json()["temporary_password"] is None
    login = client.post(
        "/api/v1/auth/login", json={"email": "boss@dealiq.com", "password": "Password123!"}
    )
    assert login.status_code == 200


def test_create_user_rejects_duplicate_email(client, as_role, make_user):
    make_user(email="dup@dealiq.com")
    as_role(Role.admin)
    r = client.post("/api/v1/users", json={"email": "dup@dealiq.com", "role": "analyste"})
    assert r.status_code == 409


def test_create_user_requires_admin(client, as_role):
    as_role(Role.senior)
    r = client.post("/api/v1/users", json={"email": "x@dealiq.com", "role": "analyste"})
    assert r.status_code == 403


def test_deactivate_and_reactivate_is_audited(client, db_session, as_role):
    admin = as_role(Role.admin)
    target = User(email="tgt@dealiq.com", hashed_password="x", role=Role.entrepreneur)
    db_session.add(target)
    db_session.commit()
    db_session.refresh(target)

    r = client.patch(f"/api/v1/users/{target.id}/active", json={"is_active": False})
    assert r.status_code == 200
    assert r.json()["is_active"] is False

    r = client.patch(f"/api/v1/users/{target.id}/active", json={"is_active": True})
    assert r.status_code == 200
    assert r.json()["is_active"] is True

    logs = (
        db_session.query(AuditLog)
        .filter(AuditLog.action == AuditAction.account_status_changed)
        .all()
    )
    assert len(logs) == 2
    assert all(log.actor_id == admin.id for log in logs)


def test_admin_cannot_deactivate_self(client, as_role):
    admin = as_role(Role.admin)
    r = client.patch(f"/api/v1/users/{admin.id}/active", json={"is_active": False})
    assert r.status_code == 400


def test_admin_cannot_demote_self(client, as_role):
    admin = as_role(Role.admin)
    r = client.patch(f"/api/v1/users/{admin.id}/role", json={"role": "analyste"})
    assert r.status_code == 400


def test_login_failure_is_audited(client, db_session):
    client.post("/api/v1/auth/register", json={"email": "z@dealiq.com", "password": "Password123!"})
    client.post("/api/v1/auth/login", json={"email": "z@dealiq.com", "password": "bad"})
    failures = (
        db_session.query(AuditLog).filter(AuditLog.action == AuditAction.login_failed).all()
    )
    assert len(failures) == 1
    assert failures[0].actor_email == "z@dealiq.com"
