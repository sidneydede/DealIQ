"""Génération PDF serveur (fpdf2). Mini-rapport readiness (M6) — conforme §11.

Polices cœur (Helvetica) = latin-1 : on neutralise les caractères typographiques
hors latin-1 (em-dash, points de suspension, guillemets courbes…).
"""
from __future__ import annotations

from datetime import UTC, datetime

from fpdf import FPDF

_REPLACEMENTS = {
    "—": "-", "–": "-", "…": "...", "’": "'",
    "‘": "'", "“": '"', "”": '"', "€": "EUR", " ": " ",
}


def _safe(text: str) -> str:
    for k, v in _REPLACEMENTS.items():
        text = text.replace(k, v)
    return text.encode("latin-1", "replace").decode("latin-1")


def _watermark(pdf: FPDF) -> None:
    pdf.set_font("Helvetica", "B", 48)
    pdf.set_text_color(232, 232, 232)
    with pdf.rotation(45, x=105, y=160):
        pdf.text(45, 165, "CONFIDENTIEL")
    pdf.set_text_color(0, 0, 0)


def _h1(pdf: FPDF, text: str) -> None:
    pdf.set_font("Helvetica", "B", 16)
    pdf.multi_cell(0, 9, _safe(text), new_x="LMARGIN", new_y="NEXT")


def _section(pdf: FPDF, text: str) -> None:
    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(40, 70, 130)
    pdf.multi_cell(0, 7, _safe(text), new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(0, 0, 0)


def _line(pdf: FPDF, text: str, size: int = 11) -> None:
    pdf.set_font("Helvetica", "", size)
    pdf.multi_cell(0, 6, _safe(text), new_x="LMARGIN", new_y="NEXT")


def _bullets(pdf: FPDF, items: list[str]) -> None:
    pdf.set_font("Helvetica", "", 11)
    if not items:
        _line(pdf, "Aucun.", 11)
        return
    for it in items:
        pdf.multi_cell(0, 6, _safe(f"- {it}"), new_x="LMARGIN", new_y="NEXT")


def report_pdf(data: dict) -> bytes:
    """Rend le mini-rapport readiness (dict de services.report.build) en PDF (bytes)."""
    pdf = FPDF(format="A4")
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.set_margins(18, 16, 18)
    pdf.add_page()
    _watermark(pdf)

    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(0, 6, _safe("DealIQ - Mini-rapport readiness"), new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(0, 0, 0)
    pdf.ln(1)

    _h1(pdf, data.get("company_name") or "Entreprise")

    confidence = data.get("confidence")
    conf_txt = f" (confiance {round(confidence * 100)}%)" if confidence is not None else ""
    _line(pdf, f"Catégorie : {data.get('category_label', '-')}{conf_txt}")
    if data.get("deal_type"):
        dt = data["deal_type"]
        _line(pdf, f"Type de deal : {getattr(dt, 'value', dt)}")
    _line(pdf, f"Instrument recommandé : {data.get('recommended_instrument', '-')}")

    _section(pdf, "Points bloquants")
    _bullets(pdf, data.get("blockers", []))

    _section(pdf, "Chemin vers la bancabilité")
    _bullets(pdf, data.get("path_to_bankable", []))

    if data.get("alternative_suggestion"):
        _section(pdf, "Suggestion alternative")
        _line(pdf, data["alternative_suggestion"])

    _section(pdf, "Services recommandés")
    _bullets(pdf, data.get("recommended_services", []))

    pdf.ln(3)
    pdf.set_draw_color(200, 200, 200)
    pdf.line(18, pdf.get_y(), 192, pdf.get_y())
    pdf.ln(2)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(110, 110, 110)
    for d in data.get("disclaimers", []):
        pdf.multi_cell(0, 4.5, _safe(d), new_x="LMARGIN", new_y="NEXT")
    stamp = datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")
    pdf.multi_cell(0, 4.5, _safe(f"Document généré le {stamp}. Confidentiel."),
                   new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(0, 0, 0)

    out = pdf.output()
    return bytes(out)
