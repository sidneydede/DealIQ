"""Tests de l'adaptateur e-mail : mode mock + mode SMTP réel (monkeypatché)."""
from __future__ import annotations

import smtplib

from app.domain import email_template
from app.services import email as email_adapter


def test_email_template_renders_and_escapes():
    html = email_template.render("Bonjour <b>", "Ligne 1\nLigne 2 & fin")
    assert html.startswith("<!doctype html>")
    assert "DealIQ" in html
    assert "Bonjour &lt;b&gt;" in html  # titre échappé
    assert "Ligne 1<br>Ligne 2 &amp; fin" in html  # newline → <br>, & échappé


def test_send_email_records_html_in_mock(monkeypatch):
    monkeypatch.setattr(email_adapter.settings, "email_provider", "mock")
    email_adapter.send_email("a@dealiq.com", "S", "B", html="<p>hi</p>")
    assert email_adapter.SENT[-1]["html"] == "<p>hi</p>"


class _FakeSMTP:
    """Faux serveur SMTP capturant le message, sans aucun accès réseau."""

    last: _FakeSMTP | None = None

    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = port
        self.tls = False
        self.login_user = None
        self.sent = []
        _FakeSMTP.last = self

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def starttls(self):
        self.tls = True

    def login(self, user, password):
        self.login_user = user

    def send_message(self, msg):
        self.sent.append(msg)


def test_mock_mode_records_without_network(monkeypatch):
    monkeypatch.setattr(email_adapter.settings, "email_provider", "mock")
    before = len(email_adapter.SENT)
    email_adapter.send_email("a@dealiq.com", "Sujet", "Corps")
    assert len(email_adapter.SENT) == before + 1
    assert email_adapter.SENT[-1]["to"] == "a@dealiq.com"


def test_smtp_mode_sends_message(monkeypatch):
    monkeypatch.setattr(email_adapter.settings, "email_provider", "smtp")
    monkeypatch.setattr(email_adapter.settings, "smtp_host", "smtp.example.com")
    monkeypatch.setattr(email_adapter.settings, "smtp_use_tls", True)
    monkeypatch.setattr(email_adapter.settings, "smtp_user", "user")
    monkeypatch.setattr(email_adapter.settings, "smtp_password", "secret")
    monkeypatch.setattr(email_adapter.settings, "email_from", "noreply@dealiq.com")
    monkeypatch.setattr(smtplib, "SMTP", _FakeSMTP)

    email_adapter.send_email("dest@dealiq.com", "Bienvenue", "Votre accès est prêt.")

    sent = _FakeSMTP.last
    assert sent is not None and sent.host == "smtp.example.com"
    assert sent.tls is True and sent.login_user == "user"
    assert len(sent.sent) == 1
    msg = sent.sent[0]
    assert msg["To"] == "dest@dealiq.com"
    assert msg["From"] == "noreply@dealiq.com"
    assert msg["Subject"] == "Bienvenue"
    assert "Votre accès est prêt." in msg.get_content()


def test_smtp_without_host_does_not_raise(monkeypatch):
    monkeypatch.setattr(email_adapter.settings, "email_provider", "smtp")
    monkeypatch.setattr(email_adapter.settings, "smtp_host", "")
    # Ne doit pas lever : un échec d'e-mail ne casse jamais l'action métier.
    email_adapter.send_email("x@dealiq.com", "S", "B")


def test_smtp_failure_is_swallowed(monkeypatch):
    def _boom(*a, **k):
        raise OSError("connexion refusée")

    monkeypatch.setattr(email_adapter.settings, "email_provider", "smtp")
    monkeypatch.setattr(email_adapter.settings, "smtp_host", "smtp.example.com")
    monkeypatch.setattr(smtplib, "SMTP", _boom)
    # L'exception SMTP est capturée et journalisée, jamais propagée.
    email_adapter.send_email("x@dealiq.com", "S", "B")
