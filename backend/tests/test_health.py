def test_root(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json()["app"] == "DealIQ"


def test_health(client):
    resp = client.get("/api/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_health_db(client):
    resp = client.get("/api/health/db")
    assert resp.status_code == 200
    assert resp.json()["db"] == "reachable"
