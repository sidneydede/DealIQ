"""Tests M23 — programmes sponsorisés + reporting d'impact agrégé."""
from app.api.deps import get_current_user
from app.core.security import hash_password
from app.domain.enums import AuditAction, Role
from app.main import app
from app.models.audit import AuditLog
from app.models.user import User


def _user(db, email, role=Role.entrepreneur):
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        return existing
    u = User(email=email, hashed_password=hash_password("x"), role=role)
    db.add(u)
    db.commit()
    db.refresh(u)
    return u


def _auth(user):
    app.dependency_overrides[get_current_user] = lambda: user


def _clear():
    app.dependency_overrides.pop(get_current_user, None)


def _company(client, name):
    return client.post(
        "/api/v1/companies", json={"name": name, "country": "CI", "sector": "Agro"}
    ).json()["company"]["id"]


def test_program_requires_cabinet(client, db_session):
    _auth(_user(db_session, "e@dealiq.com"))
    r = client.post("/api/v1/programs", json={"name": "P1", "sponsor_name": "DFI"})
    assert r.status_code == 403
    _clear()


def test_program_cohort_and_anonymized_report(client, db_session):
    # entreprises de la cohorte
    _auth(_user(db_session, "e@dealiq.com"))
    c1 = _company(client, "Alpha")
    c2 = _company(client, "Beta")

    # compte sponsor (avant création du programme pour la liaison)
    sponsor = _user(db_session, "dfi@dealiq.com", Role.sponsor)

    _auth(_user(db_session, "s@dealiq.com", Role.senior))
    # ESG sur une entreprise
    client.put(
        f"/api/v1/companies/{c1}/esg",
        json={"jobs_total": 50, "jobs_female": 20, "women_in_leadership": True},
    )
    prog = client.post(
        "/api/v1/programs",
        json={"name": "Prog DFI", "sponsor_name": "DFI Ouest", "sponsor_email": "dfi@dealiq.com"},
    ).json()
    assert prog["sponsor_user_id"] == sponsor.id
    assert (
        db_session.query(AuditLog).filter(AuditLog.action == AuditAction.program_created).count()
        == 1
    )

    client.post(f"/api/v1/programs/{prog['id']}/members", json={"company_id": c1})
    client.post(f"/api/v1/programs/{prog['id']}/members", json={"company_id": c2})

    # vue cabinet : membres avec noms
    members = client.get(f"/api/v1/programs/{prog['id']}/members").json()
    assert {m["company_name"] for m in members} == {"Alpha", "Beta"}

    # reporting agrégé/anonymisé (aucun nom d'entreprise dans le schéma)
    report = client.get(f"/api/v1/programs/{prog['id']}/report").json()
    assert report["cohort_size"] == 2
    assert report["by_status"]["brouillon"] == 2
    assert report["esg"]["jobs_total"] == 50
    assert report["esg"]["female_ratio"] == 0.4
    assert "company_name" not in str(report)

    # le sponsor voit SON programme et son reporting
    _auth(sponsor)
    assert len(client.get("/api/v1/programs").json()) == 1
    assert client.get(f"/api/v1/programs/{prog['id']}/report").status_code == 200
    # mais pas la liste nominative des membres (réservée cabinet)
    assert client.get(f"/api/v1/programs/{prog['id']}/members").status_code == 403
    _clear()


def test_sponsor_sees_only_own_programs(client, db_session):
    s1 = _user(db_session, "dfi1@dealiq.com", Role.sponsor)
    _user(db_session, "dfi2@dealiq.com", Role.sponsor)

    _auth(_user(db_session, "s@dealiq.com", Role.senior))
    client.post(
        "/api/v1/programs",
        json={"name": "P1", "sponsor_name": "DFI1", "sponsor_email": "dfi1@dealiq.com"},
    )
    client.post(
        "/api/v1/programs",
        json={"name": "P2", "sponsor_name": "DFI2", "sponsor_email": "dfi2@dealiq.com"},
    )

    _auth(s1)
    own = client.get("/api/v1/programs").json()
    assert len(own) == 1 and own[0]["name"] == "P1"
    _clear()
