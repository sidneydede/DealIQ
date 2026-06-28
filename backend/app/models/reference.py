"""Référentiels paramétrables (Admin) — notamment les types de deal (M24)."""
from __future__ import annotations

from sqlalchemy import JSON, Integer, String, Text
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.domain.enums import DealTypeCode, Instrument
from app.models.base import Base, TimestampMixin, UUIDMixin


class DealType(UUIDMixin, TimestampMixin, Base):
    """Référentiel des types de deal (M24).

    Donnée structurante : pilote checklist documentaire, branches de questionnaire,
    gabarit de teaser et grille de scoring. Paramétrable sans redéploiement (NFR).
    """

    __tablename__ = "deal_types"

    code: Mapped[DealTypeCode] = mapped_column(
        SAEnum(DealTypeCode, name="deal_type_code"), unique=True, nullable=False
    )
    label: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    instruments: Mapped[list] = mapped_column(JSON, default=list)  # list[Instrument]
    target_financiers: Mapped[str | None] = mapped_column(Text)

    # Pilotage du parcours (paramétrable) — listes/structures JSON
    doc_checklist: Mapped[list] = mapped_column(JSON, default=list)
    questionnaire_branch: Mapped[dict] = mapped_column(JSON, default=dict)
    teaser_template: Mapped[str | None] = mapped_column(String(120))
    scoring_weights: Mapped[dict] = mapped_column(JSON, default=dict)

    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(default=True)

    @property
    def primary_instrument(self) -> Instrument | None:
        return Instrument(self.instruments[0]) if self.instruments else None
