"""Schémas Pydantic pour les notifications."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.domain.enums import NotificationType


class NotificationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    type: NotificationType
    title: str
    body: str
    link: str | None
    object_type: str | None
    object_id: str | None
    read_at: datetime | None
    created_at: datetime


class UnreadCount(BaseModel):
    count: int
