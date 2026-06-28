"""Entités Company, Contact, FinancingNeed (CDC §8.3, M2/M3/M24)."""
from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Numeric, String, Text
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.enums import (
    CompanyStage,
    CompanyStatus,
    Country,
    Currency,
    DataReliability,
    DealTypeCode,
)
from app.models.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.models.score import Score


class Company(UUIDMixin, TimestampMixin, Base):
    """Fiche entreprise — base maître des PME (M2). Actif propriétaire du Cabinet."""

    __tablename__ = "companies"

    # Identité (RG-M2-02 : nom, pays, secteur obligatoires à la création)
    name: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    country: Mapped[Country] = mapped_column(SAEnum(Country, name="country"), nullable=False)
    sector: Mapped[str] = mapped_column(String(120), nullable=False)
    rccm: Mapped[str | None] = mapped_column(String(120), index=True)  # clé d'unicité RG-M2-01

    stage: Mapped[CompanyStage | None] = mapped_column(SAEnum(CompanyStage, name="company_stage"))
    status: Mapped[CompanyStatus] = mapped_column(
        SAEnum(CompanyStatus, name="company_status"),
        default=CompanyStatus.brouillon,
        nullable=False,
    )

    # Données financières déclaratives (fourchette) — label « déclaré / non audité » (RG-M2-04)
    revenue_min: Mapped[float | None] = mapped_column(Numeric(18, 2))
    revenue_max: Mapped[float | None] = mapped_column(Numeric(18, 2))
    currency: Mapped[Currency] = mapped_column(
        SAEnum(Currency, name="currency"), default=Currency.XOF, nullable=False
    )
    financials_reliability: Mapped[DataReliability] = mapped_column(
        SAEnum(DataReliability, name="data_reliability"),
        default=DataReliability.declare_non_audite,
        nullable=False,
    )

    # Propriétaire (entrepreneur). Lié à un User.
    owner_id: Mapped[str | None] = mapped_column(ForeignKey("users.id"), index=True)

    contacts: Mapped[list[Contact]] = relationship(
        back_populates="company", cascade="all, delete-orphan"
    )
    financing_need: Mapped[FinancingNeed | None] = relationship(
        back_populates="company", uselist=False, cascade="all, delete-orphan"
    )
    score: Mapped[Score | None] = relationship(
        back_populates="company", uselist=False, cascade="all, delete-orphan"
    )


class Contact(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "contacts"

    company_id: Mapped[str] = mapped_column(ForeignKey("companies.id"), index=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str | None] = mapped_column(String(120))
    email: Mapped[str | None] = mapped_column(String(255))
    phone: Mapped[str | None] = mapped_column(String(50))
    kyc_done: Mapped[bool] = mapped_column(Boolean, default=False)  # checklist manuelle MVP

    company: Mapped[Company] = relationship(back_populates="contacts")


class FinancingNeed(UUIDMixin, TimestampMixin, Base):
    """Besoin de financement + type de deal principal/secondaire (M24, RG-M24-01)."""

    __tablename__ = "financing_needs"

    company_id: Mapped[str] = mapped_column(
        ForeignKey("companies.id"), unique=True, index=True, nullable=False
    )
    amount: Mapped[float | None] = mapped_column(Numeric(18, 2))
    currency: Mapped[Currency] = mapped_column(
        SAEnum(Currency, name="currency"), default=Currency.XOF
    )
    use_of_funds: Mapped[str | None] = mapped_column(Text)
    horizon: Mapped[str | None] = mapped_column(String(120))

    # Type de deal — obligatoire avant scoring (RG-M24-01)
    deal_type_primary: Mapped[DealTypeCode | None] = mapped_column(
        SAEnum(DealTypeCode, name="deal_type_code")
    )
    deal_type_secondary: Mapped[DealTypeCode | None] = mapped_column(
        SAEnum(DealTypeCode, name="deal_type_code")  # optionnel (RG-M24-05)
    )

    company: Mapped[Company] = relationship(back_populates="financing_need")
