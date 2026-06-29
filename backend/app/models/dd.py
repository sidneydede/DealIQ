"""DD OHADA/SYSCOHADA (M18) : import de balance + analyse retraitée."""
from __future__ import annotations

from sqlalchemy import JSON, ForeignKey, Integer, String, Text
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.domain.enums import DealTypeCode
from app.models.base import Base, TimestampMixin, UUIDMixin


class SyscohadaImport(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "syscohada_imports"

    company_id: Mapped[str] = mapped_column(ForeignKey("companies.id"), index=True, nullable=False)
    fiscal_year: Mapped[str | None] = mapped_column(String(12))
    lines: Mapped[list] = mapped_column(JSON, default=list)  # [{account, label, amount}]
    version: Mapped[int] = mapped_column(Integer, default=1)
    imported_by: Mapped[str | None] = mapped_column(ForeignKey("users.id"))


class DdAnalysis(UUIDMixin, TimestampMixin, Base):
    """Résultat de la DD : retraitements (avec règles/sources), axes et synthèse."""

    __tablename__ = "dd_analyses"

    company_id: Mapped[str] = mapped_column(ForeignKey("companies.id"), index=True, nullable=False)
    import_id: Mapped[str | None] = mapped_column(ForeignKey("syscohada_imports.id"))
    deal_type: Mapped[DealTypeCode | None] = mapped_column(
        SAEnum(DealTypeCode, name="deal_type_code")
    )
    class_totals: Mapped[dict] = mapped_column(JSON, default=dict)
    retraitements: Mapped[dict] = mapped_column(JSON, default=dict)  # {key: {value, rule, sources}}
    focus: Mapped[list] = mapped_column(JSON, default=list)
    synthesis: Mapped[str | None] = mapped_column(Text)
    grid_version: Mapped[str | None] = mapped_column(String(40))
