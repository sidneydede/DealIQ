"""Contrôles KYC/KYB/AML (M15). Preuves conservées (RG-M15-03)."""
from __future__ import annotations

from sqlalchemy import JSON, ForeignKey, String, Text
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.domain.enums import KycCheckType, KycStatus, KycSubjectType
from app.models.base import Base, TimestampMixin, UUIDMixin


class KycCheck(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "kyc_checks"

    subject_type: Mapped[KycSubjectType] = mapped_column(
        SAEnum(KycSubjectType, name="kyc_subject_type"), nullable=False
    )
    subject_id: Mapped[str] = mapped_column(String(36), index=True, nullable=False)
    subject_label: Mapped[str | None] = mapped_column(String(255))  # nom au moment du contrôle
    check_type: Mapped[KycCheckType] = mapped_column(
        SAEnum(KycCheckType, name="kyc_check_type"), nullable=False
    )
    status: Mapped[KycStatus] = mapped_column(
        SAEnum(KycStatus, name="kyc_status"), default=KycStatus.en_attente, nullable=False
    )
    provider: Mapped[str | None] = mapped_column(String(60))
    result: Mapped[dict] = mapped_column(JSON, default=dict)  # preuve (RG-M15-03)
    notes: Mapped[str | None] = mapped_column(Text)
    checked_by: Mapped[str | None] = mapped_column(ForeignKey("users.id"))
