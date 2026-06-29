"""Tests M14 — Q&A rattaché à une mise en relation."""
from app.api.deps import get_current_user
from app.core.security import hash_password
from app.domain.enums import Role
from app.main import app
from app.models.user import User


def _user(db, email, role=Role.entrepreneur):
    u = User(email=email, hashed_password=hash_password("x"), role=role)
    db.add(u)
    db.commit()
    db.refresh(u)
    return u


def _auth(user):
    app.dependency_overrides[get_current_user] = lambda: user


def _clear():
    app.dependency_overrides.pop(get_current_user, None)


def _setup_interaction(client, db_session, fund_email="fund@dealiq.com"):
    """Entreprise investor-ready → teaser publié → investisseur lié → intérêt."""
    _auth(_user(db_session, "e@dealiq.com"))
    cid = client.post(
        "/api/v1/companies", json={"name": "Acme", "country": "CI", "sector": "Agro"}
    ).json()["company"]["id"]
    client.post(
        f"/api/v1/companies/{cid}/deal-type",
        json={"deal_type_primary": "ouverture_capital", "amount": 80000000},
    )
    client.post(f"/api/v1/companies/{cid}/score")

    # le compte investisseur doit exister AVANT la création de la fiche (pour la liaison)
    fund = _user(db_session, fund_email, Role.investisseur)

    _auth(_user(db_session, "a@dealiq.com", Role.analyste))
    client.patch(f"/api/v1/companies/{cid}/status", json={"status": "investor_ready"})
    tid = client.post(f"/api/v1/companies/{cid}/teaser").json()["id"]
    client.post(f"/api/v1/teasers/{tid}/publish")
    client.post(
        "/api/v1/investors",
        json={"name": "Fund", "type": "equity_pe_vc", "user_email": fund_email},
    )

    _auth(fund)
    iid = client.post(f"/api/v1/teasers/{tid}/interest", json={}).json()["id"]
    return iid, fund


def test_investor_sees_own_interactions(client, db_session):
    iid, fund = _setup_interaction(client, db_session)
    _auth(fund)
    mine = client.get("/api/v1/interactions").json()
    assert len(mine) == 1 and mine[0]["id"] == iid
    _clear()


def test_qa_flow(client, db_session):
    iid, fund = _setup_interaction(client, db_session)

    # investisseur pose une question
    _auth(fund)
    q = client.post(
        f"/api/v1/interactions/{iid}/qa", json={"question": "Quel est le taux de croissance ?"}
    )
    assert q.status_code == 201 and q.json()["status"] == "ouverte"
    qid = q.json()["id"]

    # cabinet répond
    _auth(_user(db_session, "s@dealiq.com", Role.senior))
    a = client.post(f"/api/v1/qa/{qid}/answer", json={"answer": "≈ 25 % par an."})
    assert a.status_code == 200 and a.json()["status"] == "repondue"
    assert a.json()["answer"].startswith("≈")

    # l'investisseur voit la réponse dans le fil
    _auth(fund)
    thread = client.get(f"/api/v1/interactions/{iid}/qa").json()
    assert len(thread) == 1 and thread[0]["answer"] is not None
    _clear()


def test_qa_access_control(client, db_session):
    iid, _ = _setup_interaction(client, db_session)
    # un autre investisseur (sans lien) n'accède pas au fil
    _auth(_user(db_session, "other@dealiq.com", Role.investisseur))
    assert client.get(f"/api/v1/interactions/{iid}/qa").status_code == 403
    assert client.post(
        f"/api/v1/interactions/{iid}/qa", json={"question": "Curieux ?"}
    ).status_code == 403
    _clear()


def test_only_cabinet_answers(client, db_session):
    iid, fund = _setup_interaction(client, db_session)
    _auth(fund)
    qid = client.post(
        f"/api/v1/interactions/{iid}/qa", json={"question": "Question ?"}
    ).json()["id"]
    # l'investisseur ne peut pas répondre (réservé cabinet)
    assert client.post(f"/api/v1/qa/{qid}/answer", json={"answer": "x"}).status_code == 403

    # cabinet clôt
    _auth(_user(db_session, "s@dealiq.com", Role.senior))
    closed = client.patch(f"/api/v1/qa/{qid}/close")
    assert closed.status_code == 200 and closed.json()["status"] == "cloturee"
    _clear()
