"""Tests Phase 3 — import texte brut, deck PDF, questions guidées."""

import io

MINIMAL = {"name": "Acme", "sector": "Fintech", "stage": "mvp", "country": "ci"}


def _create(client, headers, **extra):
    return client.post("/api/deals", json={**MINIMAL, **extra}, headers=headers).json()


def _make_pdf(text: str) -> bytes:
    """Construit un PDF minimal mono-page contenant `text` (lisible par pypdf)."""
    content = f"BT /F1 18 Tf 30 120 Td ({text}) Tj ET".encode("latin-1")
    objs = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 300 200] /Contents 4 0 R "
        b"/Resources << /Font << /F1 5 0 R >> >> >>",
        b"<< /Length %d >>\nstream\n" % len(content) + content + b"\nendstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]
    out = io.BytesIO()
    out.write(b"%PDF-1.4\n")
    offsets = []
    for i, o in enumerate(objs, start=1):
        offsets.append(out.tell())
        out.write(b"%d 0 obj\n" % i + o + b"\nendobj\n")
    xref_pos = out.tell()
    out.write(b"xref\n0 %d\n0000000000 65535 f \n" % (len(objs) + 1))
    for off in offsets:
        out.write(b"%010d 00000 n \n" % off)
    out.write(
        b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF"
        % (len(objs) + 1, xref_pos)
    )
    return out.getvalue()


# ── Extracteur (unitaire) ────────────────────────────────────────────────────
def test_extract_fields_rich():
    from app.services.text_extraction import extract_fields

    text = "Startup Fintech basée à Abidjan, fondée par Awa Diop. MVP, lève 50 millions FCFA."
    fields = {e.field: e.value for e in extract_fields(text)}
    assert fields["sector"] == "Fintech"
    assert fields["country"] == "CI"
    assert fields["stage"] == "mvp"
    assert "Awa Diop" in fields["founders"]
    assert "non audité" in fields["description"]


def test_extract_fields_empty_when_no_signal():
    from app.services.text_extraction import extract_fields

    assert extract_fields("blabla texte sans aucune information utile ici") == []


# ── Import texte brut ────────────────────────────────────────────────────────
def test_extract_text_requires_auth(client):
    assert client.post("/api/deals/1/extract-text", json={"text": "x" * 30}).status_code == 401


def test_extract_text_too_short(client, auth_headers):
    deal = _create(client, auth_headers)
    r = client.post(
        f"/api/deals/{deal['id']}/extract-text", json={"text": "court"}, headers=auth_headers
    )
    assert r.status_code == 400
    assert "plus long" in r.json()["detail"]


def test_extract_text_over_max_rejected(client, auth_headers):
    deal = _create(client, auth_headers)
    r = client.post(
        f"/api/deals/{deal['id']}/extract-text",
        json={"text": "a" * 2001},
        headers=auth_headers,
    )
    assert r.status_code == 422


def test_extract_text_produces_proposals_and_accept(client, auth_headers):
    deal = _create(client, auth_headers)
    text = "Agritech à Dakar, fondée par Moussa Ba, traction avec 200 clients."
    r = client.post(
        f"/api/deals/{deal['id']}/extract-text", json={"text": text}, headers=auth_headers
    )
    assert r.status_code == 200
    body = r.json()
    assert body["run"]["status"] == "done"
    assert all(p["source"] == "pasted_text" for p in body["proposals"])
    assert all(p["label"] == "Extrait de texte collé — non vérifié" for p in body["proposals"])

    sector_prop = next(p for p in body["proposals"] if p["field"] == "sector")
    client.post(f"/api/proposals/{sector_prop['id']}/accept", headers=auth_headers)
    refreshed = client.get(f"/api/deals/{deal['id']}", headers=auth_headers).json()
    assert refreshed["sector"] == "Agritech"


def test_extract_text_no_structured_info(client, auth_headers):
    deal = _create(client, auth_headers)
    r = client.post(
        f"/api/deals/{deal['id']}/extract-text",
        json={"text": "rien de structuré dans ce message un peu long mais vide de sens"},
        headers=auth_headers,
    )
    body = r.json()
    assert body["run"]["status"] == "no_source"
    assert body["proposals"] == []
    assert "Aucune information" in body["message"]


# ── Deck PDF ─────────────────────────────────────────────────────────────────
def test_deck_pdf_extraction(client, auth_headers):
    deal = _create(client, auth_headers)
    pdf = _make_pdf("Edtech a Abidjan, fondee par Awa Diop, traction")
    r = client.post(
        f"/api/deals/{deal['id']}/deck",
        files={"file": ("deck.pdf", pdf, "application/pdf")},
        headers=auth_headers,
    )
    assert r.status_code == 200
    body = r.json()
    assert body["run"]["status"] == "done"
    assert all(p["source"] == "deck_pdf" for p in body["proposals"])
    fields = {p["field"] for p in body["proposals"]}
    assert "sector" in fields  # Edtech détecté


def test_deck_invalid_pdf(client, auth_headers):
    deal = _create(client, auth_headers)
    r = client.post(
        f"/api/deals/{deal['id']}/deck",
        files={"file": ("x.pdf", b"not a pdf at all", "application/pdf")},
        headers=auth_headers,
    )
    assert r.status_code == 400


def test_deck_no_text(client, auth_headers, monkeypatch):
    monkeypatch.setattr(
        "app.api.routes.ingest.extract_text_from_pdf", lambda data: ""
    )
    deal = _create(client, auth_headers)
    r = client.post(
        f"/api/deals/{deal['id']}/deck",
        files={"file": ("deck.pdf", b"%PDF-1.4 fake", "application/pdf")},
        headers=auth_headers,
    )
    body = r.json()
    assert body["run"]["status"] == "no_source"
    assert "PDF" in body["message"]


# ── Questions guidées ────────────────────────────────────────────────────────
def test_guided_questions(client, auth_headers):
    deal = _create(client, auth_headers)  # description/founders/website vides, pas de twitter
    qs = client.get(f"/api/deals/{deal['id']}/guided-questions", headers=auth_headers).json()
    fields = {q["field"] for q in qs}
    assert "description" in fields
    assert "x_twitter" in fields
    assert "sector" not in fields  # déjà rempli


def test_guided_questions_shrink_after_fill(client, auth_headers):
    deal = _create(client, auth_headers, description="paiement mobile")
    qs = client.get(f"/api/deals/{deal['id']}/guided-questions", headers=auth_headers).json()
    assert "description" not in {q["field"] for q in qs}
