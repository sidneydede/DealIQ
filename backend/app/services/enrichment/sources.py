"""Adaptateurs de sources d'enrichissement — implémentation `mock`.

Les données simulées sont déterministes (dérivées de la fiche) et réalistes
pour le contexte CI/UEMOA. Le mode `live` (vraies API) lèvera l'implémentation
réelle en Phase ultérieure ; ici il renvoie un résultat d'erreur explicite.
"""

from datetime import UTC, datetime, timedelta

from app.domain.enrichment import (
    LABEL_AI_TO_VERIFY,
    LABEL_CRUNCHBASE_ABSENT,
    LABEL_DECLARED,
    LABEL_LINKEDIN_COMPANY_PRIVATE,
    LABEL_LINKEDIN_FOUNDER_PRIVATE,
    LABEL_SOCIAL_PRIVATE,
    Confidence,
    SourceCode,
    SourceStatus,
)
from app.domain.enums import SocialNetwork
from app.services.enrichment.base import (
    ActivitySignal,
    EnrichmentContext,
    EnrichmentSource,
    FieldProposal,
    SourceResult,
)


def _live_unavailable(code: str) -> SourceResult:
    return SourceResult(
        code=code,
        status=SourceStatus.ERROR,
        label="Mode live non disponible (aucune clé configurée)",
    )


def _is_private(value: str | None) -> bool:
    return bool(value) and "private" in value.lower()


class XSource(EnrichmentSource):
    """Étape 1 — X / Twitter via API v2 (source la plus enrichissable)."""

    code = SourceCode.X_API
    step = 1

    def is_applicable(self, ctx: EnrichmentContext) -> bool:
        return ctx.has_network(SocialNetwork.X_TWITTER.value)

    def fetch(self, ctx: EnrichmentContext) -> SourceResult:
        if ctx.mode == "live":
            return _live_unavailable(self.code)
        handle = ctx.first(SocialNetwork.X_TWITTER.value)
        last_activity = datetime.now(UTC) - timedelta(days=12)
        return SourceResult(
            code=self.code,
            status=SourceStatus.OK,
            activity=ActivitySignal(
                network=SocialNetwork.X_TWITTER.value, last_activity_at=last_activity
            ),
            proposals=[
                FieldProposal(
                    field="description",
                    value=f"{ctx.name} — solution mobile pour le marché ouest-africain "
                    f"(bio X {handle}).",
                    source=self.code,
                    confidence=Confidence.MOYEN,
                    label=LABEL_AI_TO_VERIFY,
                ),
                FieldProposal(
                    field="sector",
                    value="Fintech",
                    source=self.code,
                    confidence=Confidence.FAIBLE,
                    label=LABEL_AI_TO_VERIFY,
                ),
            ],
        )


class LinkedInFounderSource(EnrichmentSource):
    """Étape 2 — LinkedIn fondateur(s), extraction HTML page publique."""

    code = SourceCode.LINKEDIN_FOUNDER
    step = 2

    def is_applicable(self, ctx: EnrichmentContext) -> bool:
        return ctx.has_network(SocialNetwork.LINKEDIN_FOUNDER.value)

    def fetch(self, ctx: EnrichmentContext) -> SourceResult:
        if ctx.mode == "live":
            return _live_unavailable(self.code)
        if _is_private(ctx.first(SocialNetwork.LINKEDIN_FOUNDER.value)):
            return SourceResult(
                code=self.code,
                status=SourceStatus.PRIVATE,
                label=LABEL_LINKEDIN_FOUNDER_PRIVATE,
            )
        return SourceResult(
            code=self.code,
            status=SourceStatus.OK,
            proposals=[
                FieldProposal(
                    field="founders",
                    value="Fondateur confirmé via LinkedIn — 4 ans d'expérience "
                    "dans le secteur, ancien d'un opérateur télécom régional.",
                    source=self.code,
                    confidence=Confidence.ELEVE,
                    label=LABEL_AI_TO_VERIFY,
                )
            ],
        )


class LinkedInCompanySource(EnrichmentSource):
    """Étape 3 — LinkedIn entreprise, extraction HTML page publique."""

    code = SourceCode.LINKEDIN_COMPANY
    step = 3

    def is_applicable(self, ctx: EnrichmentContext) -> bool:
        return ctx.has_network(SocialNetwork.LINKEDIN_COMPANY.value)

    def fetch(self, ctx: EnrichmentContext) -> SourceResult:
        if ctx.mode == "live":
            return _live_unavailable(self.code)
        if _is_private(ctx.first(SocialNetwork.LINKEDIN_COMPANY.value)):
            return SourceResult(
                code=self.code,
                status=SourceStatus.PRIVATE,
                label=LABEL_LINKEDIN_COMPANY_PRIVATE,
            )
        return SourceResult(
            code=self.code,
            status=SourceStatus.OK,
            proposals=[
                FieldProposal(
                    field="description",
                    value=f"{ctx.name} — entreprise déclarée sur LinkedIn, "
                    "équipe de 2 à 10 personnes, basée à Abidjan.",
                    source=self.code,
                    confidence=Confidence.MOYEN,
                    label=LABEL_AI_TO_VERIFY,
                ),
                FieldProposal(
                    field="sector",
                    value="SaaS B2B",
                    source=self.code,
                    confidence=Confidence.MOYEN,
                    label=LABEL_AI_TO_VERIFY,
                ),
            ],
        )


class WebsiteSource(EnrichmentSource):
    """Étape 4 — Site web, scraping HTML (proposition de valeur, équipe, produit)."""

    code = SourceCode.WEBSITE
    step = 4

    def is_applicable(self, ctx: EnrichmentContext) -> bool:
        return bool(ctx.website_url)

    def fetch(self, ctx: EnrichmentContext) -> SourceResult:
        if ctx.mode == "live":
            return _live_unavailable(self.code)
        return SourceResult(
            code=self.code,
            status=SourceStatus.OK,
            proposals=[
                FieldProposal(
                    field="description",
                    value=f"Proposition de valeur extraite du site : {ctx.name} "
                    "simplifie l'accès au service pour les PME de la zone UEMOA.",
                    source=self.code,
                    confidence=Confidence.MOYEN,
                    label=LABEL_AI_TO_VERIFY,
                )
            ],
        )


class SocialOgSource(EnrichmentSource):
    """Étape 5 — Facebook / Instagram, métadonnées Open Graph uniquement."""

    code = SourceCode.FACEBOOK_OG  # code par défaut ; chaque proposition précise sa source
    step = 5

    def is_applicable(self, ctx: EnrichmentContext) -> bool:
        return ctx.has_network(SocialNetwork.FACEBOOK.value) or ctx.has_network(
            SocialNetwork.INSTAGRAM.value
        )

    def fetch(self, ctx: EnrichmentContext) -> SourceResult:
        if ctx.mode == "live":
            return _live_unavailable(self.code)
        proposals: list[FieldProposal] = []
        for network, code in (
            (SocialNetwork.FACEBOOK.value, SourceCode.FACEBOOK_OG),
            (SocialNetwork.INSTAGRAM.value, SourceCode.INSTAGRAM_OG),
        ):
            value = ctx.first(network)
            if not value:
                continue
            if _is_private(value):
                return SourceResult(
                    code=code, status=SourceStatus.PRIVATE, label=LABEL_SOCIAL_PRIVATE
                )
            proposals.append(
                FieldProposal(
                    field="description",
                    value=f"Présence {network} active (Open Graph) : {ctx.name}.",
                    source=code,
                    confidence=Confidence.FAIBLE,
                    label=LABEL_AI_TO_VERIFY,
                )
            )
        return SourceResult(
            code=self.code, status=SourceStatus.OK, proposals=proposals
        )


class CrunchbaseSource(EnrichmentSource):
    """Étape 6 — Crunchbase Basic. Données absentes pour ~70% des startups CI/UEMOA."""

    code = SourceCode.CRUNCHBASE
    step = 6

    def is_applicable(self, ctx: EnrichmentContext) -> bool:
        return bool(ctx.name)  # matchable par nom

    def fetch(self, ctx: EnrichmentContext) -> SourceResult:
        if ctx.mode == "live":
            return _live_unavailable(self.code)
        # Cas réaliste par défaut : startup absente de Crunchbase.
        # Le marqueur "[CB]" dans le nom simule un cas où la donnée existe.
        if "[CB]" not in ctx.name:
            return SourceResult(
                code=self.code,
                status=SourceStatus.NO_DATA,
                label=LABEL_CRUNCHBASE_ABSENT,
            )
        return SourceResult(
            code=self.code,
            status=SourceStatus.OK,
            proposals=[
                FieldProposal(
                    field="description",
                    value="Pre-seed levé (montant déclaré non audité), 1 investisseur.",
                    source=self.code,
                    confidence=Confidence.MOYEN,
                    label=LABEL_DECLARED,
                )
            ],
        )


# Ordre d'exécution figé (étapes 1 à 6). L'étape 7 (LLM) est gérée à part.
SOURCE_PIPELINE: list[EnrichmentSource] = [
    XSource(),
    LinkedInFounderSource(),
    LinkedInCompanySource(),
    WebsiteSource(),
    SocialOgSource(),
    CrunchbaseSource(),
]
