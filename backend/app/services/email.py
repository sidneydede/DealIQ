"""Adaptateur e-mail. Mode mock par défaut (aucune clé externe requise).

Branchable plus tard sur un vrai fournisseur (Resend / Amazon SES / SMTP) en
implémentant `_send_real` et en basculant `settings.email_provider`.
"""
from __future__ import annotations

import logging

from app.config import settings

logger = logging.getLogger("dealiq.email")

# Journal en mémoire des e-mails « envoyés » en mode mock (tests / debug).
SENT: list[dict] = []


def send_email(to: str, subject: str, body: str) -> None:
    """Envoie (ou simule) un e-mail. Ne lève jamais : un échec d'e-mail ne doit
    pas casser l'action métier qui l'a déclenché."""
    if settings.email_provider == "mock":
        SENT.append({"to": to, "subject": subject, "body": body})
        logger.info("[email mock] to=%s subject=%s", to, subject)
        return
    try:  # pragma: no cover - branchement réel hors périmètre MVP
        _send_real(to, subject, body)
    except Exception:  # noqa: BLE001
        logger.exception("Échec d'envoi e-mail vers %s", to)


def _send_real(to: str, subject: str, body: str) -> None:  # pragma: no cover
    raise NotImplementedError("Aucun fournisseur e-mail réel n'est branché (mode mock).")
