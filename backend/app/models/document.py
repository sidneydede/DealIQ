"""Entité Document (M4). Sensibilité critique : hash d'intégrité + statut de vérification."""
from __future__ import annotations

from sqlalchemy import Enum as SAEnum
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.domain.enums import DocumentStatus
from app.models.base import Base, TimestampMixin, UUIDMixin


class Document(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "documents"

    company_id: Mapped[str] = mapped_column(ForeignKey("companies.id"), index=True, nullable=False)
    doc_type: Mapped[str] = mapped_column(String(120), nullable=False)  # RCCM, statuts, EF, BP…
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    content_type: Mapped[str | None] = mapped_column(String(120))
    size_bytes: Mapped[int | None] = mapped_column(Integer)
    storage_key: Mapped[str | None] = mapped_column(String(512))  # clé stockage objet (S3)
    sha256: Mapped[str | None] = mapped_column(String(64))  # intégrité (RG-M4-02)
    version: Mapped[int] = mapped_column(Integer, default=1)
    status: Mapped[DocumentStatus] = mapped_column(
        SAEnum(DocumentStatus, name="document_status"),
        default=DocumentStatus.recu,
        nullable=False,
    )
    uploaded_by: Mapped[str | None] = mapped_column(ForeignKey("users.id"))
