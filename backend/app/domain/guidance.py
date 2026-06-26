"""Guidage produit : notes pédagogiques, périmètre, critère de succès MVP.

Centralise le contenu non-technique imposé par le CDC :
- règle d'or #6 : chaque étape clé affiche une note pédagogique (max 2 lignes) ;
- périmètre strict : tout ce qui est hors scope est listé explicitement.
"""

# Note pédagogique par étape clé (≤ 2 lignes à l'écran)
PEDAGOGICAL_NOTES = {
    "create_deal": (
        "Saisis d'abord ce que tu sais : une fiche incomplète vaut mieux qu'un deal oublié."
    ),
    "data_zero": (
        "Aucune donnée publique ? Cherche au moins le @Twitter ou le LinkedIn du fondateur — "
        "c'est souvent la seule source disponible en CI."
    ),
    "completeness": (
        "Le score mesure la complétude de la fiche, pas la qualité du deal. "
        "Vise ≥ 61 pour un enrichissement utile."
    ),
    "social_primary": (
        "En CI/UEMOA, les réseaux publics sont la source primaire, pas un bonus. "
        "Le @Twitter en premier."
    ),
    "enrich": (
        "L'IA propose, tu décides. Chaque donnée produite par l'IA est à vérifier "
        "avant de l'accepter."
    ),
    "validation": (
        "Accepte, modifie ou rejette champ par champ. Rien n'est écrit sur la fiche sans toi."
    ),
    "traction": (
        "Toute traction déclarée est « non auditée » par défaut. Ne suppose jamais le contraire."
    ),
    "crunchbase": (
        "Crunchbase est une option, pas une dépendance : ~70 % des startups early stage "
        "CI/UEMOA y sont absentes."
    ),
}

# Périmètre produit — strictement délimité (cf. CDC)
SCOPE = {
    "in_scope": [
        "Sourcing 100 % manuel des deals",
        "Enrichissement assisté par IA (Agent A), validé champ par champ",
        "Import de contenu social brut (texte collé) et de deck PDF",
        "Notes de deal et historique des modifications",
    ],
    "out_of_scope": [
        "Scoring / notation de deal",
        "Pipeline management",
        "Due diligence (DD)",
        "Comité d'investissement (IC)",
        "Matching automatique deal ↔ fonds",
        "Veille / scraping proactif, flux push de deals",
        "Suivi post-investissement",
        "Recherche par nom sur les réseaux sociaux",
    ],
}

# Critère de succès du MVP (mesurable, 1 phrase)
MVP_SUCCESS_CRITERION = (
    "Un analyste crée une fiche, lance l'enrichissement et valide au moins un champ "
    "de bout en bout en moins de 10 minutes, sans assistance."
)

# Mots-clés interdits dans les routes (garde-fou hors-scope)
FORBIDDEN_ROUTE_KEYWORDS = [
    "scoring",
    "score-deal",
    "pipeline",
    "due-diligence",
    "matching",
    "watch",
    "veille",
    "crawl",
    "scrape",
]
