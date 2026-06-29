"""Profil ESG / impact (M19). Champs optionnels sauf cible DFI (RG-M19-01)."""
from __future__ import annotations

from sqlalchemy import Boolean, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin, UUIDMixin


class EsgProfile(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "esg_profiles"

    company_id: Mapped[str] = mapped_column(
        ForeignKey("companies.id"), unique=True, index=True, nullable=False
    )

    # Emplois / social
    jobs_total: Mapped[int | None] = mapped_column(Integer)
    jobs_female: Mapped[int | None] = mapped_column(Integer)
    jobs_youth: Mapped[int | None] = mapped_column(Integer)
    women_in_leadership: Mapped[bool | None] = mapped_column(Boolean)

    # Climat / environnement
    environmental_policy: Mapped[bool | None] = mapped_column(Boolean)
    climate_risk_assessed: Mapped[bool | None] = mapped_column(Boolean)

    # Gouvernance
    governance_formalized: Mapped[bool | None] = mapped_column(Boolean)
    board_independent: Mapped[bool | None] = mapped_column(Boolean)

    # Obligatoire si programme DFI/sponsorisé (RG-M19-01)
    esg_required: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    # Anti impact-washing : justification par pièces quand c'est possible (RG-M19-02)
    evidence_note: Mapped[str | None] = mapped_column(Text)
    notes: Mapped[str | None] = mapped_column(Text)
