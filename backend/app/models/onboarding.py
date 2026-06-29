"""Session d'onboarding / questionnaire (M3). Autosave + reprise + consentement horodaté."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin, UUIDMixin


class OnboardingSession(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "onboarding_sessions"

    company_id: Mapped[str] = mapped_column(
        ForeignKey("companies.id"), unique=True, index=True, nullable=False
    )
    answers: Mapped[dict] = mapped_column(JSON, default=dict)  # {question_id: valeur}
    current_step: Mapped[int] = mapped_column(Integer, default=0)  # reprise (RG-M3-02)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)

    # Consentement explicite horodaté (RG-M3-04)
    consent_given: Mapped[bool] = mapped_column(Boolean, default=False)
    consent_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    consent_text: Mapped[str | None] = mapped_column(Text)

    # Résultat de gating à la soumission (RG-M3-03)
    gating_route: Mapped[str | None] = mapped_column(String(40))
