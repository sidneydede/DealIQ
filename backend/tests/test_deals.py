"""Tests API du Module 1 — Sourcing manuel."""

MINIMAL = {"name": "Acme", "sector": "Fintech", "stage": "mvp", "country": "ci"}


def test_create_requires_auth(client):
    assert client.post("/api/deals", json=MINIMAL).status_code == 401


def test_create_minimal(client, auth_headers):
    resp = client.post("/api/deals", json=MINIMAL, headers=auth_headers)
    assert resp.status_code == 201
    body = resp.json()
    assert body["completeness_score"] == 50
    assert body["country"] == "CI"  # normalisé en majuscules
    assert body["score_band"].startswith("Fiche partielle")
    assert body["data_zero_mode"] is False


def test_create_with_socials_scores_extra(client, auth_headers):
    payload = {**MINIMAL, "socials": [{"network": "x_twitter", "value": "@acme"}]}
    resp = client.post("/api/deals", json=payload, headers=auth_headers)
    assert resp.status_code == 201
    assert resp.json()["completeness_score"] == 56  # 50 + 6


def test_data_zero_mode(client, auth_headers):
    payload = {**MINIMAL, "deck_status": "non"}
    resp = client.post("/api/deals", json=payload, headers=auth_headers)
    body = resp.json()
    assert body["data_zero_mode"] is True
    assert "@Twitter" in body["data_zero_hint"]


def test_invalid_stage_rejected(client, auth_headers):
    payload = {**MINIMAL, "stage": "series-a"}
    assert client.post("/api/deals", json=payload, headers=auth_headers).status_code == 422


def test_patch_records_history(client, auth_headers):
    deal_id = client.post("/api/deals", json=MINIMAL, headers=auth_headers).json()["id"]

    resp = client.patch(
        f"/api/deals/{deal_id}",
        json={"website_url": "https://acme.ci", "description": "Paiement mobile"},
        headers=auth_headers,
    )
    assert resp.status_code == 200
    assert resp.json()["completeness_score"] == 60  # 50 + 5 (url) + 5 (desc)

    history = client.get(f"/api/deals/{deal_id}/history", headers=auth_headers).json()
    changed = {h["field"] for h in history}
    assert {"website_url", "description", "completeness_score"} <= changed
    url_entry = next(h for h in history if h["field"] == "website_url")
    assert url_entry["old_value"] is None
    assert url_entry["new_value"] == "https://acme.ci"


def test_patch_socials_replace_and_log(client, auth_headers):
    deal_id = client.post("/api/deals", json=MINIMAL, headers=auth_headers).json()["id"]
    resp = client.patch(
        f"/api/deals/{deal_id}",
        json={"socials": [{"network": "linkedin_founder", "value": "https://lnkd/x"}]},
        headers=auth_headers,
    )
    assert resp.json()["completeness_score"] == 55  # 50 + 5
    history = client.get(f"/api/deals/{deal_id}/history", headers=auth_headers).json()
    assert any(h["field"] == "social:linkedin_founder" for h in history)


def test_notes_crud(client, auth_headers):
    deal_id = client.post("/api/deals", json=MINIMAL, headers=auth_headers).json()["id"]
    r = client.post(
        f"/api/deals/{deal_id}/notes",
        json={"content": "Vu au HUB Abidjan, fondateur ex-Orange."},
        headers=auth_headers,
    )
    assert r.status_code == 201
    notes = client.get(f"/api/deals/{deal_id}/notes", headers=auth_headers).json()
    assert len(notes) == 1
    assert "HUB Abidjan" in notes[0]["content"]


def test_list_and_get_and_delete(client, auth_headers):
    deal_id = client.post("/api/deals", json=MINIMAL, headers=auth_headers).json()["id"]
    assert len(client.get("/api/deals", headers=auth_headers).json()) == 1
    assert client.get(f"/api/deals/{deal_id}", headers=auth_headers).status_code == 200
    assert client.delete(f"/api/deals/{deal_id}", headers=auth_headers).status_code == 204
    assert client.get(f"/api/deals/{deal_id}", headers=auth_headers).status_code == 404


def test_note_too_long_rejected(client, auth_headers):
    deal_id = client.post("/api/deals", json=MINIMAL, headers=auth_headers).json()["id"]
    r = client.post(
        f"/api/deals/{deal_id}/notes",
        json={"content": "x" * 1001},
        headers=auth_headers,
    )
    assert r.status_code == 422
