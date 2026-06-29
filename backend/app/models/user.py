"""Entité User (CDC §8.3, M1)."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.domain.enums import Role
from app.models.base import Base, TimestampMixin, UUIDMixin


class User(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str | None] = mapped_column(String(255))
    role: Mapped[Role] = mapped_column(
        SAEnum(Role, native_enum=False), default=Role.entrepreneur, nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    mfa_enabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    # Secret TOTP (base32). Renseigné à l'enrôlement, effacé à la désactivation.
    mfa_secret: Mapped[str | None] = mapped_column(String(64))
    # Validation e-mail par OTP (US-M1-02) à l'auto-inscription.
    email_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    email_otp: Mapped[str | None] = mapped_column(String(6))
    email_otp_expires: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
