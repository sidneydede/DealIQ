"""Contrats communs des sources d'enrichissement.

Chaque source implémente la même interface et peut tourner en mode `mock`
(données simulées réalistes CI/UEMOA) ou `live` (vraies API — Phase ultérieure).
Brancher une vraie API ne change que l'implémentation de `fetch`, pas le reste.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime

from app.domain.enrichment import SourceCode, SourceStatus

# Champs de la fiche pouvant recevoir une proposition (colonnes scalaires du Deal)
WRITABLE_FIELDS = {
    "description",
    "sector",
    "founders",
    "stage",
    "country",
    "website_url",
}

# Champs que l'étape 7 (LLM) peut inférer si encore vides (cf. CDC)
INFERABLE_FIELDS = ["sector", "stage", "country"]


@dataclass
class FieldProposal:
    field: str
    value: str
    source: str            # SourceCode
    confidence: str        # Confidence
    label: str | None = None


@dataclass
class ActivitySignal:
    network: str
    last_activity_at: datetime


@dataclass
class SourceResult:
    code: str
    status: str            # SourceStatus
    label: str | None = None
    proposals: list[FieldProposal] = field(default_factory=list)
    activity: ActivitySignal | None = None


@dataclass
class EnrichmentContext:
    """Vue en lecture seule des données de la fiche, passée aux sources."""

    name: str
    sector: str | None
    stage: str | None
    country: str | None
    description: str | None
    founders: str | None
    website_url: str | None
    socials: dict[str, list[str]]  # network -> valeurs
    mode: str = "mock"

    def has_network(self, network: str) -> bool:
        return bool(self.socials.get(network))

    def first(self, network: str) -> str | None:
        vals = self.socials.get(network)
        return vals[0] if vals else None


class EnrichmentSource(ABC):
    code: SourceCode
    step: int

    @abstractmethod
    def is_applicable(self, ctx: EnrichmentContext) -> bool:
        """Vrai si le champ requis par cette étape est renseigné."""

    @abstractmethod
    def fetch(self, ctx: EnrichmentContext) -> SourceResult:
        """Collecte les données et retourne des propositions à valider."""

    def skipped(self) -> SourceResult:
        return SourceResult(code=self.code, status=SourceStatus.SKIPPED)
