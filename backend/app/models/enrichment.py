"""Entités d'enrichissement (Agent A).

Les modèles sont définis dès la Phase 1 pour figer le data model complet ;
leur comportement (orchestrateur, adaptateurs sources) arrive en Phase 2.
"""

from datetime import datetime

from sqlalchemy import ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class EnrichmentRun(Base):
    """Historique de chaque exécution d'Agent A sur une fiche."""

    __tablename__ = "enrichment_runs"

    id: Mapped[int] = mapped_column(primary_key=True)
    deal_id: Mapped[int] = mapped_column(
        ForeignKey("deals.id", ondelete="CASCADE"), nullable=False, index=True
    )
    # queued | running | done | failed | no_source
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="queued")
    started_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )
    finished_at: Mapped[datetime | None] = mapped_column(nullable=True)
    # Résumé technique (étapes exécutées, erreurs) — JSON sérialisé en texte
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)

    proposals: Mapped[list["EnrichmentProposal"]] = relationship(
        back_populates="run", cascade="all, delete-orphan", passive_deletes=True
    )


class EnrichmentProposal(Base):
    """Suggestion produite par Agent A, en attente de validation humaine.

    Aucun champ de la fiche n'est jamais écrasé automatiquement : l'analyste
    accepte / modifie / rejette chaque proposition individuellement.
    """

    __tablename__ = "enrichment_proposals"

    id: Mapped[int] = mapped_column(primary_key=True)
    deal_id: Mapped[int] = mapped_column(
        ForeignKey("deals.id", ondelete="CASCADE"), nullable=False, index=True
    )
    run_id: Mapped[int] = mapped_column(
        ForeignKey("enrichment_runs.id", ondelete="CASCADE"), nullable=False, index=True
    )
    field: Mapped[str] = mapped_column(String(60), nullable=False)
    suggested_value: Mapped[str | None] = mapped_column(Text, nullable=True)
    # x_api | linkedin_founder | linkedin_company | website | facebook_og |
    # instagram_og | crunchbase | llm_inference | pasted_text
    source: Mapped[str] = mapped_column(String(40), nullable=False)
    confidence: Mapped[str] = mapped_column(String(10), nullable=False)  # faible|moyen|eleve
    label: Mapped[str | None] = mapped_column(String(120), nullable=True)
    collected_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )
    # pending | accepted | modified | rejected
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending")

    run: Mapped["EnrichmentRun"] = relationship(back_populates="proposals")
