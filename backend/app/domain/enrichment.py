"""Constantes métier de l'enrichissement (Agent A — Module 2).

Aligné sur le cahier des charges : sources, labels obligatoires, anti-rate-limit,
seuil d'activité, et table des fallbacks (source / condition / comportement / label).
"""

from enum import StrEnum

# Délai minimum entre deux enrichissements sur la même fiche (anti rate-limit)
RATE_LIMIT_MINUTES = 30

# Au-delà, le signal d'activité sociale est grisé
ACTIVITY_STALE_DAYS = 90


class SourceCode(StrEnum):
    """Identifiant de la source exacte d'une proposition."""

    X_API = "x_api"
    LINKEDIN_FOUNDER = "linkedin_founder"
    LINKEDIN_COMPANY = "linkedin_company"
    WEBSITE = "website"
    FACEBOOK_OG = "facebook_og"
    INSTAGRAM_OG = "instagram_og"
    CRUNCHBASE = "crunchbase"
    LLM_INFERENCE = "llm_inference"
    PASTED_TEXT = "pasted_text"


class Confidence(StrEnum):
    FAIBLE = "faible"
    MOYEN = "moyen"
    ELEVE = "eleve"


class ProposalStatus(StrEnum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    MODIFIED = "modified"
    REJECTED = "rejected"


class RunStatus(StrEnum):
    QUEUED = "queued"
    RUNNING = "running"
    DONE = "done"
    FAILED = "failed"
    NO_SOURCE = "no_source"  # fallback total : aucune source exploitable


class SourceStatus(StrEnum):
    """Résultat d'exécution d'une source individuelle."""

    OK = "ok"
    SKIPPED = "skipped"        # champ requis absent
    PRIVATE = "private"        # profil/page privé
    NO_DATA = "no_data"        # accessible mais rien d'exploitable
    ERROR = "error"


# ── Labels obligatoires (cf. règles d'or du CDC) ─────────────────────────────
LABEL_AI_TO_VERIFY = "IA — à vérifier"
LABEL_DECLARED = "Déclaré / non audité"
LABEL_LLM_INFERENCE = "Inférence IA — fiabilité faible — vérifier impérativement"
LABEL_LINKEDIN_FOUNDER_PRIVATE = "Profil LinkedIn privé — données non accessibles"
LABEL_LINKEDIN_COMPANY_PRIVATE = "Page LinkedIn privée — données non accessibles"
LABEL_SOCIAL_PRIVATE = "Page privée — enrichissement impossible"
LABEL_CRUNCHBASE_ABSENT = "Données Crunchbase absentes pour cette startup"

# Message de fallback total (étapes 1-6 échouées, LLM insuffisant)
FALLBACK_TOTAL_MESSAGE = (
    "Enrichissement automatique impossible. Aucune source accessible. "
    "Complète la fiche manuellement ou ajoute au moins un @Twitter."
)

# Message prérequis non rempli
PREREQUISITE_MESSAGE = (
    "Ajoute au moins un @Twitter ou une URL pour démarrer "
    "l'enrichissement automatique."
)

# Table documentaire des fallbacks (exposée via l'API) :
# source / condition déclenchante / comportement / label affiché
FALLBACK_TABLE = [
    {
        "source": SourceCode.X_API,
        "condition": "Aucun @handle X fourni",
        "behavior": "Étape ignorée",
        "label": None,
    },
    {
        "source": SourceCode.LINKEDIN_FOUNDER,
        "condition": "Profil LinkedIn fondateur restreint / privé",
        "behavior": "0 champ extrait",
        "label": LABEL_LINKEDIN_FOUNDER_PRIVATE,
    },
    {
        "source": SourceCode.LINKEDIN_COMPANY,
        "condition": "Page LinkedIn entreprise privée",
        "behavior": "0 champ extrait",
        "label": LABEL_LINKEDIN_COMPANY_PRIVATE,
    },
    {
        "source": SourceCode.WEBSITE,
        "condition": "URL site web absente ou injoignable",
        "behavior": "Étape ignorée / 0 champ",
        "label": None,
    },
    {
        "source": SourceCode.FACEBOOK_OG,
        "condition": "Page Facebook/Instagram privée",
        "behavior": "0 champ extrait",
        "label": LABEL_SOCIAL_PRIVATE,
    },
    {
        "source": SourceCode.CRUNCHBASE,
        "condition": "Startup absente de Crunchbase (~70% en CI/UEMOA)",
        "behavior": "0 champ extrait",
        "label": LABEL_CRUNCHBASE_ABSENT,
    },
    {
        "source": SourceCode.LLM_INFERENCE,
        "condition": "Champs encore vides après étapes 1-6, données textuelles dispo",
        "behavior": "Inférence sur champs vides uniquement",
        "label": LABEL_LLM_INFERENCE,
    },
    {
        "source": "all",
        "condition": "Étapes 1-6 échouées + LLM insuffisant",
        "behavior": "Aucune inférence, formulaire manuel guidé proposé",
        "label": FALLBACK_TOTAL_MESSAGE,
    },
]
