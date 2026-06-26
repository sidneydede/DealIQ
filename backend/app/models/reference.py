"""Données de référence CI/UEMOA (tables de lookup, remplies au seed).

Ces tables servent à alimenter les listes déroulantes du Module 1 et à
documenter l'écosystème cible. Elles ne contiennent aucune logique métier.
"""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Country(Base):
    """Pays / zone géographique (UEMOA + Afrique de l'Ouest)."""

    __tablename__ = "ref_countries"

    id: Mapped[int] = mapped_column(primary_key=True)
    iso2: Mapped[str] = mapped_column(String(2), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    is_uemoa: Mapped[bool] = mapped_column(default=False, nullable=False)


class Sector(Base):
    """Secteur / verticale."""

    __tablename__ = "ref_sectors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)


class Fund(Base):
    """Fonds VC actif sur la zone (référence pédagogique)."""

    __tablename__ = "ref_funds"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    country: Mapped[str | None] = mapped_column(String(100), nullable=True)


class Accelerator(Base):
    """Accélérateur / incubateur de l'écosystème."""

    __tablename__ = "ref_accelerators"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    country: Mapped[str | None] = mapped_column(String(100), nullable=True)


class DealSourceType(Base):
    """Canaux de sourcing (événement / WhatsApp / recommandation / ...)."""

    __tablename__ = "ref_deal_source_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(40), unique=True, nullable=False)
    label: Mapped[str] = mapped_column(String(100), nullable=False)
