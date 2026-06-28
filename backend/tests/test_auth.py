def _register(client, email="e@dealiq.com", password="Password123!"):
    return client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": password, "full_name": "Test"},
    )


def test_register_and_login_flow(client):
    r = _register(client)
    assert r.status_code == 201
    assert r.json()["role"] == "entrepreneur"

    # email en doublon -> 409
    assert _register(client).status_code == 409

    r = client.post(
        "/api/v1/auth/login",
        json={"email": "e@dealiq.com", "password": "Password123!"},
    )
    assert r.status_code == 200
    tokens = r.json()
    assert "access_token" in tokens and "refresh_token" in tokens

    # /me avec le token
    me = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {tokens['access_token']}"},
    )
    assert me.status_code == 200
    assert me.json()["email"] == "e@dealiq.com"


def test_login_wrong_password(client):
    _register(client)
    r = client.post(
        "/api/v1/auth/login",
        json={"email": "e@dealiq.com", "password": "wrong"},
    )
    assert r.status_code == 401


def test_refresh_rotates_tokens(client):
    _register(client)
    tokens = client.post(
        "/api/v1/auth/login",
        json={"email": "e@dealiq.com", "password": "Password123!"},
    ).json()
    r = client.post("/api/v1/auth/refresh", json={"refresh_token": tokens["refresh_token"]})
    assert r.status_code == 200
    assert "access_token" in r.json()


def test_me_requires_auth(client):
    assert client.get("/api/v1/auth/me").status_code == 401


def test_refresh_rejects_access_token(client):
    _register(client)
    tokens = client.post(
        "/api/v1/auth/login",
        json={"email": "e@dealiq.com", "password": "Password123!"},
    ).json()
    # un access token ne doit pas être accepté comme refresh
    r = client.post("/api/v1/auth/refresh", json={"refresh_token": tokens["access_token"]})
    assert r.status_code == 401
