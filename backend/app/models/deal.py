from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.base import TimestampMixin


class Deal(Base, TimestampMixin):
    """Fiche deal — saisie 100 % manuelle par l'analyste (Module 1)."""

    __tablename__ = "deals"

    id: Mapped[int] = mapped_column(primary_key=True)

    # ── Champs obligatoires ──────────────────────────────────────────────
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    sector: Mapped[str] = mapped_column(String(100), nullable=False)
    stage: Mapped[str] = mapped_column(String(20), nullable=False)  # Stage
    country: Mapped[str] = mapped_column(String(2), nullable=False)  # ISO2

    # ── Champs optionnels ────────────────────────────────────────────────
    founders: Mapped[str | None] = mapped_column(Text, nullable=True)
    description: Mapped[str | None] = mapped_column(String(280), nullable=True)
    deal_source: Mapped[str | None] = mapped_column(String(20), nullable=True)  # DealSource
    deal_source_other: Mapped[str | None] = mapped_column(String(120), nullable=True)
    website_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    deck_status: Mapped[str | None] = mapped_column(String(20), nullable=True)  # DeckStatus
    # Champ libre du Mode Données Zéro
    what_i_know: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # ── Traçabilité ──────────────────────────────────────────────────────
    completeness_score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # ── Signal d'activité sociale (renseigné par Agent A) ────────────────
    last_activity_network: Mapped[str | None] = mapped_column(String(30), nullable=True)
    last_activity_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # ── Relations ────────────────────────────────────────────────────────
    socials: Mapped[list["SocialProfile"]] = relationship(
        back_populates="deal", cascade="all, delete-orphan", passive_deletes=True
    )
    notes: Mapped[list["DealNote"]] = relationship(
        back_populates="deal", cascade="all, delete-orphan", passive_deletes=True
    )
    changes: Mapped[list["DealChangeLog"]] = relationship(
        back_populates="deal", cascade="all, delete-orphan", passive_deletes=True
    )


class SocialProfile(Base):
    """Profil réseau social rattaché à une fiche (un par réseau, multiple possible
    pour LinkedIn fondateur). Source primaire d'enrichissement en CI/UEMOA."""

    __tablename__ = "social_profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    deal_id: Mapped[int] = mapped_column(
        ForeignKey("deals.id", ondelete="CASCADE"), nullable=False, index=True
    )
    network: Mapped[str] = mapped_column(String(30), nullable=False)  # SocialNetwork
    value: Mapped[str] = mapped_column(String(500), nullable=False)  # URL ou @handle

    deal: Mapped["Deal"] = relationship(back_populates="socials")


class DealNote(Base):
    """Note libre horodatée (journal de deal, max 1000 caractères)."""

    __tablename__ = "deal_notes"

    id: Mapped[int] = mapped_column(primary_key=True)
    deal_id: Mapped[int] = mapped_column(
        ForeignKey("deals.id", ondelete="CASCADE"), nullable=False, index=True
    )
    content: Mapped[str] = mapped_column(String(1000), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )

    deal: Mapped["Deal"] = relationship(back_populates="notes")


class DealChangeLog(Base):
    """Historique des modifications : champ modifié, ancienne/nouvelle valeur, timestamp."""

    __tablename__ = "deal_change_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    deal_id: Mapped[int] = mapped_column(
        ForeignKey("deals.id", ondelete="CASCADE"), nullable=False, index=True
    )
    field: Mapped[str] = mapped_column(String(60), nullable=False)
    old_value: Mapped[str | None] = mapped_column(Text, nullable=True)
    new_value: Mapped[str | None] = mapped_column(Text, nullable=True)
    changed_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )

    deal: Mapped["Deal"] = relationship(back_populates="changes")
