"""Fixtures de test : base SQLite en mémoire + client FastAPI + seed minimal."""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.deps import get_current_user
from app.core.security import hash_password
from app.database import get_db
from app.domain.enums import Role
from app.main import app
from app.models import Base, User
from app.seed.seed import seed_deal_types


@pytest.fixture
def db_session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
    db = TestingSessionLocal()
    seed_deal_types(db)
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db_session):
    app.dependency_overrides[get_db] = lambda: db_session
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def make_user(db_session):
    def _make(email: str = "user@dealiq.com", password: str = "Password123!",
              role: Role = Role.entrepreneur) -> User:
        user = User(email=email, hashed_password=hash_password(password), role=role)
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        return user

    return _make


@pytest.fixture
def as_role(client, db_session):
    """Authentifie le client en injectant un utilisateur du rôle voulu."""

    def _as(role: Role) -> User:
        user = User(email=f"{role.value}@dealiq.com",
                    hashed_password=hash_password("x"), role=role)
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        app.dependency_overrides[get_current_user] = lambda: user
        return user

    yield _as
    app.dependency_overrides.pop(get_current_user, None)
