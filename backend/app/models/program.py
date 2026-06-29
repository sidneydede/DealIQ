"""Programmes sponsorisés (M23). Cohorte d'entreprises financée par un sponsor DFI/banque."""
from __future__ import annotations

from sqlalchemy import Enum as SAEnum
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.domain.enums import ProgramStatus
from app.models.base import Base, TimestampMixin, UUIDMixin


class Program(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "programs"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    sponsor_name: Mapped[str] = mapped_column(String(255), nullable=False)
    sponsor_user_id: Mapped[str | None] = mapped_column(ForeignKey("users.id"), index=True)
    scope: Mapped[str | None] = mapped_column(Text)
    deliverables: Mapped[str | None] = mapped_column(Text)
    status: Mapped[ProgramStatus] = mapped_column(
        SAEnum(ProgramStatus, native_enum=False), default=ProgramStatus.actif, nullable=False
    )
    created_by: Mapped[str | None] = mapped_column(ForeignKey("users.id"))


class ProgramMember(UUIDMixin, TimestampMixin, Base):
    """Appartenance d'une entreprise à la cohorte d'un programme."""

    __tablename__ = "program_members"

    program_id: Mapped[str] = mapped_column(ForeignKey("programs.id"), index=True, nullable=False)
    company_id: Mapped[str] = mapped_column(ForeignKey("companies.id"), index=True, nullable=False)
