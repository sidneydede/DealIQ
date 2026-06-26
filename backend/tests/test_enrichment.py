"""Tests API de l'Agent A (enrichissement mode mock) + validation."""

import pytest

MINIMAL = {"name": "Acme", "sector": "Fintech", "stage": "mvp", "country": "ci"}


def _create(client, headers, **extra):
    payload = {**MINIMAL, **extra}
    return client.post("/api/deals", json=payload, headers=headers).json()


def _with_twitter(client, headers):
    return _create(client, headers, socials=[{"network": "x_twitter", "value": "@acme"}])


def test_enrich_requires_auth(client):
    assert client.post("/api/deals/1/enrich").status_code == 401


def test_prerequisite_not_met(client, auth_headers):
    deal = _create(client, auth_headers)  # 4 champs requis, aucune URL/réseau
    r = client.post(f"/api/deals/{deal['id']}/enrich", headers=auth_headers)
    assert r.status_code == 400
    assert "@Twitter" in r.json()["detail"]


def test_enrich_produces_proposals(client, auth_headers):
    deal = _with_twitter(client, auth_headers)
    r = client.post(f"/api/deals/{deal['id']}/enrich", headers=auth_headers)
    assert r.status_code == 200
    body = r.json()
    assert body["run"]["status"] == "done"
    assert body["message"] is None
    fields = {p["field"] for p in body["proposals"]}
    assert "description" in fields
    # toutes les propositions portent une source + un niveau de confiance
    for p in body["proposals"]:
        assert p["source"]
        assert p["confidence"] in {"faible", "moyen", "eleve"}
        assert p["status"] == "pending"


def test_rate_limit_blocks_second_run(client, auth_headers):
    deal = _with_twitter(client, auth_headers)
    assert client.post(f"/api/deals/{deal['id']}/enrich", headers=auth_headers).status_code == 200
    second = client.post(f"/api/deals/{deal['id']}/enrich", headers=auth_headers)
    assert second.status_code == 429
    assert "minutes" in second.json()["detail"]


def test_accept_writes_field_and_logs(client, auth_headers):
    deal = _with_twitter(client, auth_headers)
    body = client.post(f"/api/deals/{deal['id']}/enrich", headers=auth_headers).json()
    prop = next(p for p in body["proposals"] if p["field"] == "description")

    r = client.post(f"/api/proposals/{prop['id']}/accept", headers=auth_headers)
    assert r.status_code == 200
    assert r.json()["status"] == "accepted"

    refreshed = client.get(f"/api/deals/{deal['id']}", headers=auth_headers).json()
    assert refreshed["description"] == prop["suggested_value"]

    history = client.get(f"/api/deals/{deal['id']}/history", headers=auth_headers).json()
    assert any(h["field"] == "description" for h in history)


def test_modify_writes_custom_value(client, auth_headers):
    deal = _with_twitter(client, auth_headers)
    body = client.post(f"/api/deals/{deal['id']}/enrich", headers=auth_headers).json()
    prop = next(p for p in body["proposals"] if p["field"] == "description")

    r = client.post(
        f"/api/proposals/{prop['id']}/modify",
        json={"value": "Paiement mobile pour marchés informels"},
        headers=auth_headers,
    )
    assert r.json()["status"] == "modified"
    refreshed = client.get(f"/api/deals/{deal['id']}", headers=auth_headers).json()
    assert refreshed["description"] == "Paiement mobile pour marchés informels"


def test_reject_does_not_write(client, auth_headers):
    deal = _with_twitter(client, auth_headers)
    body = client.post(f"/api/deals/{deal['id']}/enrich", headers=auth_headers).json()
    prop = next(p for p in body["proposals"] if p["field"] == "description")

    r = client.post(f"/api/proposals/{prop['id']}/reject", headers=auth_headers)
    assert r.json()["status"] == "rejected"
    refreshed = client.get(f"/api/deals/{deal['id']}", headers=auth_headers).json()
    assert refreshed["description"] is None


def test_double_resolution_conflict(client, auth_headers):
    deal = _with_twitter(client, auth_headers)
    body = client.post(f"/api/deals/{deal['id']}/enrich", headers=auth_headers).json()
    pid = body["proposals"][0]["id"]
    assert client.post(f"/api/proposals/{pid}/reject", headers=auth_headers).status_code == 200
    again = client.post(f"/api/proposals/{pid}/accept", headers=auth_headers)
    assert again.status_code == 409


def test_fallback_total_when_only_private_source(client, auth_headers):
    deal = _create(
        client,
        auth_headers,
        socials=[{"network": "linkedin_founder", "value": "https://lnkd/private-x"}],
    )
    r = client.post(f"/api/deals/{deal['id']}/enrich", headers=auth_headers)
    assert r.status_code == 200
    body = r.json()
    assert body["run"]["status"] == "no_source"
    assert body["proposals"] == []
    assert "impossible" in body["message"].lower()


def test_activity_banner_after_enrich(client, auth_headers):
    deal = _with_twitter(client, auth_headers)
    client.post(f"/api/deals/{deal['id']}/enrich", headers=auth_headers)
    refreshed = client.get(f"/api/deals/{deal['id']}", headers=auth_headers).json()
    assert refreshed["activity"] is not None
    assert refreshed["activity"]["network"] == "x_twitter"
    assert refreshed["activity"]["stale"] is False


def test_status_and_fallbacks_endpoints(client, auth_headers):
    deal = _with_twitter(client, auth_headers)
    status = client.get(f"/api/deals/{deal['id']}/enrich/status", headers=auth_headers).json()
    assert status["prerequisite_met"] is True
    assert status["can_run"] is True

    fb = client.get("/api/enrichment/fallbacks", headers=auth_headers).json()
    assert any(row["source"] == "llm_inference" for row in fb)


@pytest.mark.parametrize("empty", [["sector"], ["sector", "stage", "country"]])
def test_llm_inference_unit(empty):
    from app.services.enrichment.base import EnrichmentContext
    from app.services.enrichment.llm import infer_llm

    ctx = EnrichmentContext(
        name="X", sector=None, stage=None, country=None,
        description="desc", founders=None, website_url=None, socials={},
    )
    result = infer_llm(ctx, empty)
    assert len(result.proposals) == len(empty)
    for p in result.proposals:
        assert p.source == "llm_inference"
        assert p.confidence == "faible"
        assert "fiabilité faible" in p.label
