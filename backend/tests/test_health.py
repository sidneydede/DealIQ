def test_health(client):
    r = client.get("/api/v1/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_meta_deal_types_seeded(client):
    r = client.get("/api/v1/meta/deal-types")
    assert r.status_code == 200
    codes = {d["code"] for d in r.json()}
    assert "ouverture_capital" in codes
    assert "dette_bancaire" in codes


def test_meta_countries(client):
    r = client.get("/api/v1/meta/countries")
    assert r.status_code == 200
    data = {c["code"]: c for c in r.json()}
    assert data["CI"]["zone"] == "UEMOA"
    assert data["CI"]["currency"] == "XOF"
    assert data["CM"]["zone"] == "CEMAC"
    assert data["CM"]["currency"] == "XAF"
