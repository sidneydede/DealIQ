"""Tests des endpoints meta + garde-fou : aucune route hors périmètre."""

from app.domain.guidance import FORBIDDEN_ROUTE_KEYWORDS
from app.main import app


def test_meta_public(client):
    body = client.get("/api/meta").json()
    assert body["mvp_success_criterion"]
    assert "Scoring / notation de deal" in body["scope"]["out_of_scope"]


def test_pedagogical_notes_max_two_lines(client):
    notes = client.get("/api/meta/pedagogical-notes").json()
    assert "enrich" in notes
    # règle d'or #6 : max 2 lignes à l'écran
    for text in notes.values():
        assert text.count("\n") <= 1


def test_no_out_of_scope_routes():
    """Garde-fou : aucune route ne doit exposer une feature interdite par le CDC."""
    paths = {getattr(r, "path", "") for r in app.routes}
    for keyword in FORBIDDEN_ROUTE_KEYWORDS:
        offending = [p for p in paths if keyword in p.lower()]
        assert not offending, f"Route hors-scope détectée pour '{keyword}': {offending}"
