"""Tests de durcissement (Lot 5) — rate limiter, en-têtes, magic-bytes."""
import pytest

from app.api.deps import get_current_user
from app.core.ratelimit import RateLimiter
from app.core.security import hash_password
from app.domain.enums import Role
from app.main import app
from app.models.user import User
from app.services import documents as docsvc


@pytest.fixture(autouse=True)
def _tmp_storage(tmp_path, monkeypatch):
    monkeypatch.setattr(docsvc.settings, "storage_dir", str(tmp_path / "storage"))


def test_rate_limiter_window():
    t = {"v": 0.0}
    rl = RateLimiter(max_requests=2, window_seconds=10, clock=lambda: t["v"])
    assert rl.allow("k") is True
    assert rl.allow("k") is True
    assert rl.allow("k") is False  # 3e refusée dans la fenêtre
    t["v"] = 11  # fenêtre écoulée
    assert rl.allow("k") is True


def test_security_headers_present(client):
    r = client.get("/api/v1/health")
    assert r.headers.get("X-Content-Type-Options") == "nosniff"
    assert r.headers.get("X-Frame-Options") == "DENY"


def test_upload_rejects_content_mismatch(client, db_session):
    user = User(email="e@dealiq.com", hashed_password=hash_password("x"), role=Role.entrepreneur)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    app.dependency_overrides[get_current_user] = lambda: user

    cid = client.post(
        "/api/v1/companies", json={"name": "Acme", "country": "CI", "sector": "Agro"}
    ).json()["company"]["id"]

    # type déclaré PDF mais contenu non-PDF -> rejet (magic bytes)
    r = client.post(
        f"/api/v1/companies/{cid}/documents",
        data={"doc_type": "etats_financiers"},
        files={"file": ("faux.pdf", b"ceci-n-est-pas-un-pdf", "application/pdf")},
    )
    assert r.status_code == 422
    app.dependency_overrides.pop(get_current_user, None)
