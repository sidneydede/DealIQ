"""Référentiel investisseurs & critères (M9, CDC §8.3)."""
from __future__ import annotations

from sqlalchemy import JSON, Boolean, ForeignKey, Numeric, String
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.enums import Currency, InvestorQualifStatus, InvestorType
from app.models.base import Base, TimestampMixin, UUIDMixin


class Investor(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "investors"

    name: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    type: Mapped[InvestorType] = mapped_column(SAEnum(InvestorType, name="investor_type"))
    jurisdiction: Mapped[str | None] = mapped_column(String(120))
    team: Mapped[str | None] = mapped_column(String(255))
    qualif_status: Mapped[InvestorQualifStatus] = mapped_column(
        SAEnum(InvestorQualifStatus, name="investor_qualif_status"),
        default=InvestorQualifStatus.prospect,
        nullable=False,
    )
    # Compte utilisateur (rôle investisseur) qui gère cette fiche, le cas échéant.
    user_id: Mapped[str | None] = mapped_column(ForeignKey("users.id"), index=True)

    criteria: Mapped[InvestmentCriteria | None] = relationship(
        back_populates="investor", uselist=False, cascade="all, delete-orphan"
    )


class InvestmentCriteria(UUIDMixin, TimestampMixin, Base):
    """Critères d'investissement (filtres durs + appétence). Base du matching M10."""

    __tablename__ = "investment_criteria"

    investor_id: Mapped[str] = mapped_column(
        ForeignKey("investors.id"), unique=True, index=True, nullable=False
    )
    # Filtres durs — listes vides = « pas de restriction ».
    countries: Mapped[list] = mapped_column(JSON, default=list)  # codes pays
    sectors: Mapped[list] = mapped_column(JSON, default=list)
    instruments: Mapped[list] = mapped_column(JSON, default=list)  # Instrument
    deal_types: Mapped[list] = mapped_column(JSON, default=list)  # DealTypeCode acceptés
    stages: Mapped[list] = mapped_column(JSON, default=list)  # CompanyStage
    exclusions: Mapped[list] = mapped_column(JSON, default=list)  # secteurs/pays exclus

    ticket_min: Mapped[float | None] = mapped_column(Numeric(18, 2))
    ticket_max: Mapped[float | None] = mapped_column(Numeric(18, 2))
    ticket_currency: Mapped[Currency] = mapped_column(
        SAEnum(Currency, name="currency"), default=Currency.XOF
    )
    esg_required: Mapped[bool] = mapped_column(Boolean, default=False)

    investor: Mapped[Investor] = relationship(back_populates="criteria")
