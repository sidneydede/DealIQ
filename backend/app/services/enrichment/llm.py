"""Étape 7 — Inférence LLM (mock).

N'intervient que sur les champs encore vides après les étapes 1 à 6.
Toujours labellisée « fiabilité faible — vérifier impérativement ».
En mode `live`, branchera l'API Claude (Anthropic).
"""

from app.domain.enrichment import (
    LABEL_LLM_INFERENCE,
    Confidence,
    SourceCode,
    SourceStatus,
)
from app.services.enrichment.base import (
    EnrichmentContext,
    FieldProposal,
    SourceResult,
)

# Valeurs inférées simulées par champ
_MOCK_INFERENCE = {
    "sector": "Fintech",
    "stage": "mvp",
    "country": "CI",
}


def infer_llm(ctx: EnrichmentContext, empty_fields: list[str]) -> SourceResult:
    if ctx.mode == "live":
        return SourceResult(
            code=SourceCode.LLM_INFERENCE,
            status=SourceStatus.ERROR,
            label="Mode live non disponible (clé Claude absente)",
        )
    proposals = [
        FieldProposal(
            field=f,
            value=_MOCK_INFERENCE[f],
            source=SourceCode.LLM_INFERENCE,
            confidence=Confidence.FAIBLE,
            label=LABEL_LLM_INFERENCE,
        )
        for f in empty_fields
        if f in _MOCK_INFERENCE
    ]
    return SourceResult(
        code=SourceCode.LLM_INFERENCE,
        status=SourceStatus.OK if proposals else SourceStatus.NO_DATA,
        proposals=proposals,
    )
