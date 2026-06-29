"""Adaptateur e-mail. Mode mock par défaut (aucune clé externe requise).

Mode réel via SMTP (`settings.email_provider="smtp"` + `smtp_*`) — compatible
n'importe quel fournisseur (Amazon SES SMTP, Resend, Mailgun, Gmail…), sans
dépendance externe (bibliothèque standard `smtplib`).
"""
from __future__ import annotations

import logging
import smtplib
from email.message import EmailMessage

from app.config import settings

logger = logging.getLogger("dealiq.email")

# Journal en mémoire des e-mails « envoyés » en mode mock (tests / debug).
SENT: list[dict] = []


def send_email(to: str, subject: str, body: str, html: str | None = None) -> None:
    """Envoie (ou simule) un e-mail (texte + alternative HTML optionnelle). Ne lève
    jamais : un échec d'e-mail ne doit pas casser l'action métier qui l'a déclenché."""
    if settings.email_provider == "mock":
        SENT.append({"to": to, "subject": subject, "body": body, "html": html})
        logger.info("[email mock] to=%s subject=%s", to, subject)
        return
    try:
        _send_real(to, subject, body, html)
    except Exception:  # noqa: BLE001
        logger.exception("Échec d'envoi e-mail vers %s", to)


def _send_real(to: str, subject: str, body: str, html: str | None = None) -> None:
    """Envoi SMTP réel. Lève en cas d'échec (capté par send_email)."""
    if not settings.smtp_host:
        raise RuntimeError("SMTP non configuré (smtp_host vide).")
    msg = EmailMessage()
    msg["From"] = settings.email_from
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)
    if html:
        msg.add_alternative(html, subtype="html")
    with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=10) as smtp:
        if settings.smtp_use_tls:
            smtp.starttls()
        if settings.smtp_user:
            smtp.login(settings.smtp_user, settings.smtp_password)
        smtp.send_message(msg)
