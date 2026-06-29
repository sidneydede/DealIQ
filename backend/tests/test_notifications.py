"""Tests du centre de notifications + déclencheurs métier."""
from __future__ import annotations

from app.domain.enums import (
    InteractionStatus,
    InvestorType,
    KycCheckType,
    KycSubjectType,
    NotificationType,
    Role,
)
from app.models.investor import Investor
from app.models.qa import QAItem
from app.models.teaser import Interaction, Teaser
from app.services import email as email_adapter
from app.services import kyc as kyc_svc
from app.services import notifications as notif
from app.services import qa as qa_svc


def test_notify_creates_inapp_and_mock_email(db_session, make_user):
    user = make_user(email="recv@dealiq.com")
    before = len(email_adapter.SENT)
    notif.notify(
        db_session,
        recipient=user,
        type=NotificationType.qa_answered,
        title="Coucou",
        body="Un message",
        link="/x",
    )
    assert notif.unread_count(db_session, user) == 1
    assert len(email_adapter.SENT) == before + 1
    assert email_adapter.SENT[-1]["to"] == "recv@dealiq.com"


def test_notify_roles_excludes_author(db_session, make_user):
    author = make_user(email="auth-ana@dealiq.com", role=Role.analyste)
    other = make_user(email="other-senior@dealiq.com", role=Role.senior)
    notif.notify_roles(
        db_session,
        (Role.analyste, Role.senior),
        exclude_user_id=author.id,
        type=NotificationType.qa_asked,
        title="Q",
        body="b",
    )
    assert notif.unread_count(db_session, author) == 0
    assert notif.unread_count(db_session, other) == 1


def test_mark_read_and_read_all(db_session, make_user):
    user = make_user(email="reader@dealiq.com")
    for i in range(3):
        notif.notify(
            db_session, recipient=user, type=NotificationType.qa_asked,
            title=f"t{i}", body="b", send_email=False,
        )
    assert notif.unread_count(db_session, user) == 3
    first = notif.list_for(db_session, user)[0]
    notif.mark_read(db_session, first)
    assert notif.unread_count(db_session, user) == 2
    notif.mark_all_read(db_session, user)
    assert notif.unread_count(db_session, user) == 0


def test_kyc_hit_notifies_compliance(db_session, make_user):
    conformite = make_user(email="conf@dealiq.com", role=Role.conformite)
    admin = make_user(email="adm@dealiq.com", role=Role.admin)
    actor = make_user(email="actor-conf@dealiq.com", role=Role.conformite)
    investor = Investor(name="Groupe Sanction", type=InvestorType.equity_pe_vc)
    db_session.add(investor)
    db_session.commit()
    db_session.refresh(investor)

    kyc_svc.run_check(
        db_session, KycSubjectType.investor, investor.id,
        KycCheckType.aml_screening, actor,
    )
    for u in (conformite, admin):
        items = notif.list_for(db_session, u)
        assert any(n.type == NotificationType.kyc_hit for n in items)


def test_qa_answer_notifies_investor_owner(db_session, make_user):
    owner = make_user(email="inv-owner@dealiq.com", role=Role.investisseur)
    analyste = make_user(email="ana2@dealiq.com", role=Role.analyste)
    investor = Investor(name="Fonds Démo", type=InvestorType.equity_pe_vc, user_id=owner.id)
    teaser = Teaser(company_id="c-demo", title="Opportunité agro", sector="Agro")
    db_session.add_all([investor, teaser])
    db_session.commit()
    db_session.refresh(investor)
    db_session.refresh(teaser)
    interaction = Interaction(
        teaser_id=teaser.id, company_id="c-demo", investor_id=investor.id,
        status=InteractionStatus.interesse,
    )
    db_session.add(interaction)
    db_session.commit()
    db_session.refresh(interaction)
    item = QAItem(interaction_id=interaction.id, asked_by=owner.id, question="Quel CA ?")
    db_session.add(item)
    db_session.commit()
    db_session.refresh(item)

    qa_svc.answer(db_session, item, analyste, "Le CA est de 500 MFCFA.")
    items = notif.list_for(db_session, owner)
    assert any(n.type == NotificationType.qa_answered for n in items)


def test_notifications_endpoints(client, db_session, as_role):
    user = as_role(Role.investisseur)
    notif.notify(
        db_session, recipient=user, type=NotificationType.qa_answered,
        title="Réponse", body="…", link="/my-interactions", send_email=False,
    )
    r = client.get("/api/v1/notifications")
    assert r.status_code == 200
    assert len(r.json()) == 1

    assert client.get("/api/v1/notifications/unread-count").json()["count"] == 1

    notif_id = r.json()[0]["id"]
    assert client.post(f"/api/v1/notifications/{notif_id}/read").status_code == 200
    assert client.get("/api/v1/notifications/unread-count").json()["count"] == 0


def test_cannot_read_others_notification(client, db_session, make_user, as_role):
    other = make_user(email="someone@dealiq.com")
    n = notif.notify(
        db_session, recipient=other, type=NotificationType.qa_asked,
        title="x", body="y", send_email=False,
    )
    as_role(Role.investisseur)
    assert client.post(f"/api/v1/notifications/{n.id}/read").status_code == 404
