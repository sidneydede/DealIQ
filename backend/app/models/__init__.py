"""Point d'import unique des modèles -> utilisé par Alembic (autogenerate)."""

from app.models.deal import (
    Deal,
    DealChangeLog,
    DealNote,
    SocialProfile,
)
from app.models.enrichment import (
    EnrichmentProposal,
    EnrichmentRun,
)
from app.models.reference import (
    Accelerator,
    Country,
    DealSourceType,
    Fund,
    Sector,
)
from app.models.user import User

__all__ = [
    "User",
    "Country",
    "Sector",
    "Fund",
    "Accelerator",
    "DealSourceType",
    "Deal",
    "SocialProfile",
    "DealNote",
    "DealChangeLog",
    "EnrichmentRun",
    "EnrichmentProposal",
]
