"""Extraction de champs structurés depuis un texte libre (mock LLM, déterministe).

Réutilisé par l'import de contenu social brut (texte collé) et l'upload de deck.
En mode `live`, branchera l'API Claude ; ici, extraction par règles/regex ciblées.
"""

import re
from dataclasses import dataclass

from app.domain.enrichment import Confidence

# Secteurs reconnus (mot-clé -> libellé canonique)
_SECTOR_KEYWORDS = {
    "fintech": "Fintech",
    "agritech": "Agritech",
    "agri": "Agritech",
    "edtech": "Edtech",
    "e-commerce": "E-commerce",
    "ecommerce": "E-commerce",
    "santé": "Healthtech",
    "health": "Healthtech",
    "logistique": "Logistique / Mobilité",
    "mobilité": "Logistique / Mobilité",
    "énergie": "Energie / Cleantech",
    "energie": "Energie / Cleantech",
    "cleantech": "Energie / Cleantech",
    "assurance": "Insurtech",
    "insurtech": "Insurtech",
    "saas": "SaaS B2B",
    "marketplace": "Marketplace",
}

# Stade (mot-clé -> code Stage)
_STAGE_KEYWORDS = {
    "idée": "idee",
    "mvp": "mvp",
    "prototype": "mvp",
    "traction": "traction",
    "clients": "traction",
    "revenus": "traction",
    "scale": "scale",
}

# Villes / pays -> ISO2 (UEMOA + Afrique de l'Ouest)
_PLACE_TO_ISO = {
    "côte d'ivoire": "CI",
    "cote d'ivoire": "CI",
    "ivoire": "CI",
    "abidjan": "CI",
    "sénégal": "SN",
    "senegal": "SN",
    "dakar": "SN",
    "bénin": "BJ",
    "benin": "BJ",
    "cotonou": "BJ",
    "togo": "TG",
    "lomé": "TG",
    "lome": "TG",
    "mali": "ML",
    "bamako": "ML",
    "burkina": "BF",
    "ouagadougou": "BF",
    "niger": "NE",
    "niamey": "NE",
    "ghana": "GH",
    "nigeria": "NG",
}

_FUNDING_RE = re.compile(
    r"(\d[\d\s.,]*\s*(?:millions?|milliards?|m|k)?\s*(?:fcfa|xof|usd|\$|€|euros?|dollars?))",
    re.IGNORECASE,
)
_FOUNDER_RE = re.compile(
    r"fond[ée]e?s?\s+par\s+([A-ZÉÀ][^.,;:\n]+)", re.IGNORECASE
)


@dataclass
class ExtractedField:
    field: str
    value: str
    confidence: str


def _find_first(text_lower: str, mapping: dict[str, str]) -> str | None:
    for keyword, value in mapping.items():
        if keyword in text_lower:
            return value
    return None


def extract_fields(text: str) -> list[ExtractedField]:
    """Retourne les champs détectés. Liste vide => aucune info structurée."""
    text = text.strip()
    low = text.lower()
    found: list[ExtractedField] = []

    sector = _find_first(low, _SECTOR_KEYWORDS)
    if sector:
        found.append(ExtractedField("sector", sector, Confidence.MOYEN))

    stage = _find_first(low, _STAGE_KEYWORDS)
    if stage:
        found.append(ExtractedField("stage", stage, Confidence.FAIBLE))

    country = _find_first(low, _PLACE_TO_ISO)
    if country:
        found.append(ExtractedField("country", country, Confidence.MOYEN))

    fm = _FOUNDER_RE.search(text)
    if fm:
        found.append(ExtractedField("founders", fm.group(1).strip(), Confidence.MOYEN))

    funding = _FUNDING_RE.search(text)

    # Description : produite seulement si au moins un signal structuré a été détecté
    if found or funding:
        snippet = re.sub(r"\s+", " ", text)[:240]
        if funding:
            snippet = f"{snippet} [Traction déclarée : {funding.group(1).strip()} — non audité]"
        found.append(
            ExtractedField("description", snippet[:280], Confidence.FAIBLE)
        )

    return found
