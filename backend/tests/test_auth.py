from tests.conftest import TEST_EMAIL, TEST_PASSWORD


def test_login_ok(client):
    resp = client.post(
        "/api/auth/login",
        data={"username": TEST_EMAIL, "password": TEST_PASSWORD},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]


def test_login_wrong_password(client):
    resp = client.post(
        "/api/auth/login",
        data={"username": TEST_EMAIL, "password": "wrong"},
    )
    assert resp.status_code == 401


def test_me_requires_auth(client):
    assert client.get("/api/auth/me").status_code == 401


def test_me_with_token(client, auth_headers):
    resp = client.get("/api/auth/me", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["email"] == TEST_EMAIL


def test_me_with_bad_token(client):
    resp = client.get("/api/auth/me", headers={"Authorization": "Bearer not.a.token"})
    assert resp.status_code == 401
