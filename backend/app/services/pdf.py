"""Extraction de texte d'un deck PDF (pypdf)."""

import io

from pypdf import PdfReader


def extract_text_from_pdf(data: bytes) -> str:
    """Concatène le texte de toutes les pages. Retourne '' si rien d'extractible."""
    reader = PdfReader(io.BytesIO(data))
    parts = []
    for page in reader.pages:
        text = page.extract_text() or ""
        if text.strip():
            parts.append(text)
    return "\n".join(parts).strip()
