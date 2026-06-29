"""Gabarit HTML simple et brandé pour les e-mails (notifications, invitations)."""
from __future__ import annotations

import html as _html


def render(title: str, body: str) -> str:
    """Enveloppe HTML responsive minimaliste (inline styles, compatible clients mail)."""
    safe_title = _html.escape(title)
    safe_body = _html.escape(body).replace("\n", "<br>")
    brand = (
        '<tr><td style="padding:20px 24px 0;font-weight:700;font-size:18px;'
        'color:#2d4682;">DealIQ</td></tr>'
    )
    title_row = (
        '<tr><td style="padding:14px 24px 0;font-size:16px;font-weight:600;'
        f'color:#1a1a1a;">{safe_title}</td></tr>'
    )
    body_row = (
        '<tr><td style="padding:8px 24px 0;font-size:14px;line-height:1.5;'
        f'color:#333333;">{safe_body}</td></tr>'
    )
    footer = (
        '<tr><td style="padding:20px 24px;font-size:11px;color:#999999;">'
        "Message automatique — merci de ne pas répondre. Confidentiel.</td></tr>"
    )
    return (
        '<!doctype html><html><body style="margin:0;'
        'font-family:Arial,Helvetica,sans-serif;background:#f4f1ea;padding:24px;">'
        '<table align="center" width="100%" style="max-width:520px;margin:auto;'
        'background:#ffffff;border-radius:8px;border-collapse:separate;">'
        f"{brand}{title_row}{body_row}{footer}"
        "</table></body></html>"
    )
