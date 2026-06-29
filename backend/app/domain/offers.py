"""Catalogue d'offres d'accompagnement (M7). AUCUN prix affiché (RG-M7-01/05).

La préparation et le mandat sont chiffrés sur devis, au cas par cas, après un échange
de qualification. Seul le diagnostic d'entrée est gratuit et standard.
"""
from __future__ import annotations

ANTI_PAY_TO_PLAY = (
    "Nos services préparent votre dossier. Ils n'achètent ni un financement ni une "
    "présentation à un investisseur : seule la qualité de votre dossier décide."
)

# pricing = "gratuit" | "ticket_engagement" | "sur_devis" — jamais de montant public.
OFFERS: list[dict] = [
    {
        "key": "diagnostic",
        "label": "Diagnostic readiness",
        "pricing": "gratuit",
        "deliverables": [
            "Évaluation de votre préparation au financement",
            "Mini-rapport (catégorie, blocages, instrument adapté)",
            "Orientation vers le bon instrument",
        ],
    },
    {
        "key": "diagnostic_plus",
        "label": "Diagnostic approfondi",
        "pricing": "ticket_engagement",
        "deliverables": [
            "Rapport approfondi et plan d'action",
            "Rendez-vous de cadrage avec un consultant",
        ],
    },
    {
        "key": "preparation",
        "label": "Préparation du dossier",
        "pricing": "sur_devis",
        "deliverables": [
            "Business plan / modèle financier",
            "Valorisation",
            "Teaser et data room initiale",
        ],
    },
    {
        "key": "preparation_credit",
        "label": "Préparation d'un dossier de crédit",
        "pricing": "sur_devis",
        "deliverables": [
            "Dossier de crédit (capacité de remboursement, garanties)",
            "Plan de trésorerie et ratios",
        ],
    },
    {
        "key": "mandat",
        "label": "Mandat (levée / sourcing)",
        "pricing": "sur_devis",
        "deliverables": [
            "Mise en relation avec des investisseurs qualifiés",
            "Suivi jusqu'au closing",
        ],
    },
    {
        "key": "nurturing",
        "label": "Accompagnement amont (gratuit)",
        "pricing": "gratuit",
        "deliverables": [
            "Ressources et orientation pour mûrir le projet",
            "Réévaluation ultérieure",
        ],
    },
]

_OFFERS_BY_KEY = {o["key"]: o for o in OFFERS}


def offers_for(keys: list[str] | None = None) -> list[dict]:
    if not keys:
        return OFFERS
    return [_OFFERS_BY_KEY[k] for k in keys if k in _OFFERS_BY_KEY]
