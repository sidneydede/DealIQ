"""Tests export PDF serveur du mini-rapport readiness (M6)."""
from __future__ import annotations

from app.domain.enums import Role


def _register_login(client, email):
    client.post("/api/v1/auth/register", json={"email": email, "password": "Password123!"})
    tokens = client.post(
        "/api/v1/auth/login", json={"email": email, "password": "Password123!"}
    ).json()
    return {"Authorization": f"Bearer {tokens['access_token']}"}


def _company_with_deal_type(client, headers):
    cid = client.post(
        "/api/v1/companies",
        json={"name": "Co PDF", "country": "CI", "sector": "Agro"},
        headers=headers,
    ).json()["company"]["id"]
    client.post(
        f"/api/v1/companies/{cid}/deal-type",
        json={"deal_type_primary": "ouverture_capital", "amount": 50000000,
              "use_of_funds": "Croissance"},
        headers=headers,
    )
    return cid


def test_report_pdf_download(client):
    h = _register_login(client, "pdf-user@dealiq.com")
    cid = _company_with_deal_type(client, h)

    r = client.get(f"/api/v1/companies/{cid}/report.pdf", headers=h)
    assert r.status_code == 200
    assert r.headers["content-type"] == "application/pdf"
    assert "attachment" in r.headers["content-disposition"]
    assert ".pdf" in r.headers["content-disposition"]
    assert r.content[:5] == b"%PDF-"
    assert len(r.content) > 800  # contenu réel, pas un stub


def test_report_pdf_requires_deal_type(client):
    h = _register_login(client, "pdf-nodeal@dealiq.com")
    cid = client.post(
        "/api/v1/companies",
        json={"name": "Sans deal", "country": "SN", "sector": "Agro"},
        headers=h,
    ).json()["company"]["id"]
    assert client.get(f"/api/v1/companies/{cid}/report.pdf", headers=h).status_code == 400


def test_report_pdf_forbidden_for_investor(client, as_role):
    # Crée le dossier via un entrepreneur authentifié réellement.
    h = _register_login(client, "owner-pdf@dealiq.com")
    cid = _company_with_deal_type(client, h)
    # Bascule sur un investisseur via override d'auth.
    as_role(Role.investisseur)
    assert client.get(f"/api/v1/companies/{cid}/report.pdf").status_code == 403
