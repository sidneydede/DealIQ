"""Tests M4 — documents & checklist."""
import pytest

from app.api.deps import get_current_user
from app.core.security import hash_password
from app.domain.enums import AuditAction, Role
from app.main import app
from app.models.audit import AuditLog
from app.models.user import User
from app.services import documents as docsvc


@pytest.fixture(autouse=True)
def _tmp_storage(tmp_path, monkeypatch):
    monkeypatch.setattr(docsvc.settings, "storage_dir", str(tmp_path / "storage"))


def _user(db, email, role=Role.entrepreneur):
    u = User(email=email, hashed_password=hash_password("x"), role=role)
    db.add(u)
    db.commit()
    db.refresh(u)
    return u


def _auth(user):
    app.dependency_overrides[get_current_user] = lambda: user


def _company(client, deal_type="dette_bancaire"):
    cid = client.post(
        "/api/v1/companies", json={"name": "Acme", "country": "CI", "sector": "Agro"}
    ).json()["company"]["id"]
    client.post(f"/api/v1/companies/{cid}/deal-type", json={"deal_type_primary": deal_type})
    return cid


def _upload(client, cid, doc_type="releves_bancaires", content=b"%PDF-1.4 data",
            ctype="application/pdf", name="piece.pdf"):
    return client.post(
        f"/api/v1/companies/{cid}/documents",
        data={"doc_type": doc_type},
        files={"file": (name, content, ctype)},
    )


def test_document_content_preview_and_download(client, db_session):
    _auth(_user(db_session, "owner@dealiq.com"))
    cid = _company(client)
    did = _upload(client, cid, content=b"%PDF-1.4 hello").json()["id"]

    # Aperçu (inline) — contenu et type servis, disposition inline.
    preview = client.get(f"/api/v1/documents/{did}/content")
    assert preview.status_code == 200
    assert preview.headers["content-type"].startswith("application/pdf")
    assert preview.headers["content-disposition"].startswith("inline")
    assert preview.content == b"%PDF-1.4 hello"

    # Téléchargement (attachment).
    dl = client.get(f"/api/v1/documents/{did}/content", params={"download": "true"})
    assert dl.status_code == 200
    assert dl.headers["content-disposition"].startswith("attachment")

    # Cloisonnement : un autre entrepreneur ne peut pas accéder.
    _auth(_user(db_session, "intrus@dealiq.com"))
    assert client.get(f"/api/v1/documents/{did}/content").status_code == 403
    app.dependency_overrides.pop(get_current_user, None)


def test_upload_and_list(client, db_session):
    _auth(_user(db_session, "e@dealiq.com"))
    cid = _company(client)
    r = _upload(client, cid)
    assert r.status_code == 201
    body = r.json()
    assert body["status"] == "recu" and body["version"] == 1
    assert len(body["sha256"]) == 64

    docs = client.get(f"/api/v1/companies/{cid}/documents").json()
    assert len(docs) == 1
    app.dependency_overrides.pop(get_current_user, None)


def test_upload_rejects_bad_type(client, db_session):
    _auth(_user(db_session, "e@dealiq.com"))
    cid = _company(client)
    r = _upload(client, cid, content=b"hack", ctype="application/x-msdownload", name="x.exe")
    assert r.status_code == 422
    app.dependency_overrides.pop(get_current_user, None)


def test_versioning_increments(client, db_session):
    _auth(_user(db_session, "e@dealiq.com"))
    cid = _company(client)
    assert _upload(client, cid).json()["version"] == 1
    assert _upload(client, cid).json()["version"] == 2
    app.dependency_overrides.pop(get_current_user, None)


def test_checklist_adapts_to_deal_type(client, db_session):
    _auth(_user(db_session, "e@dealiq.com"))
    cid = _company(client, deal_type="dette_bancaire")
    _upload(client, cid, doc_type="releves_bancaires")
    items = {i["doc_type"]: i for i in client.get(
        f"/api/v1/companies/{cid}/documents/checklist").json()}
    # dette_bancaire requiert relevés, garanties, états financiers, plan de trésorerie
    assert items["releves_bancaires"]["required"] is True
    assert items["releves_bancaires"]["received"] is True
    assert items["garanties"]["required"] is True
    assert items["garanties"]["received"] is False
    app.dependency_overrides.pop(get_current_user, None)


def test_status_change_cabinet_only_and_audited(client, db_session):
    entr = _user(db_session, "e@dealiq.com")
    _auth(entr)
    cid = _company(client)
    doc_id = _upload(client, cid).json()["id"]

    # entrepreneur ne peut pas vérifier une pièce
    r = client.patch(f"/api/v1/documents/{doc_id}/status", json={"status": "verifie"})
    assert r.status_code == 403

    _auth(_user(db_session, "analyste@dealiq.com", Role.analyste))
    r = client.patch(f"/api/v1/documents/{doc_id}/status", json={"status": "verifie"})
    assert r.status_code == 200 and r.json()["status"] == "verifie"
    assert (
        db_session.query(AuditLog)
        .filter(AuditLog.action == AuditAction.document_status_changed)
        .count()
        == 1
    )
    app.dependency_overrides.pop(get_current_user, None)
