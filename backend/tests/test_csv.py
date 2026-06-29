"""Tests export CSV (dealflow cockpit + investisseurs) et helper csv_export."""
from __future__ import annotations

from app.api.deps import get_current_user
from app.core.security import hash_password
from app.domain.enums import Role
from app.main import app
from app.models.user import User
from app.services.csv_export import to_csv


def _register_login(client, email):
    client.post("/api/v1/auth/register", json={"email": email, "password": "Password123!"})
    r = client.post("/api/v1/auth/login", json={"email": email, "password": "Password123!"}).json()
    return {"Authorization": f"Bearer {r['access_token']}"}


def _as(db, role):
    u = User(email=f"{role.value}-csv@dealiq.com", hashed_password=hash_password("x"), role=role)
    db.add(u)
    db.commit()
    db.refresh(u)
    app.dependency_overrides[get_current_user] = lambda: u
    return u


def _clear():
    app.dependency_overrides.pop(get_current_user, None)


def test_to_csv_formats():
    rows = [{"a": Role.admin, "b": True, "c": None, "d": 3}]
    out = to_csv(rows, [("a", "A"), ("b", "B"), ("c", "C"), ("d", "D")])
    assert out.startswith("﻿")  # BOM Excel
    lines = out.replace("﻿", "").rstrip("\r\n").split("\r\n")
    assert lines[0] == "A;B;C;D"
    assert lines[1] == "admin;oui;;3"  # enum→value, bool→oui, None→vide


def test_cockpit_csv_requires_cabinet_and_content(client, db_session):
    h = _register_login(client, "csv-entr2@dealiq.com")
    cid = client.post(
        "/api/v1/companies",
        json={"name": "Acme CSV", "country": "CI", "sector": "Agro"},
        headers=h,
    ).json()["company"]["id"]
    client.post(
        f"/api/v1/companies/{cid}/deal-type",
        json={"deal_type_primary": "ouverture_capital", "amount": 50000000},
        headers=h,
    )

    # entrepreneur interdit
    assert client.get("/api/v1/cockpit/companies.csv", headers=h).status_code == 403

    _as(db_session, Role.analyste)
    r = client.get("/api/v1/cockpit/companies.csv")
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("text/csv")
    assert "attachment" in r.headers["content-disposition"]
    assert r.text.startswith("﻿")
    assert "Entreprise;Pays;Secteur" in r.text
    assert "Acme CSV" in r.text
    _clear()


def test_investors_csv_export(client, db_session):
    _as(db_session, Role.senior)
    client.post("/api/v1/investors", json={"name": "Sahel Capital", "type": "equity_pe_vc"})
    client.post("/api/v1/investors", json={"name": "Banque X", "type": "banque"})

    r = client.get("/api/v1/investors/export.csv")
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("text/csv")
    assert "Nom;Type;Juridiction" in r.text
    assert "Sahel Capital" in r.text and "Banque X" in r.text
    _clear()
