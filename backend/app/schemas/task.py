"""Schémas Pydantic — tâches & relances CRM (M20)."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.domain.enums import TaskStatus


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    note: str | None = None
    due_date: datetime | None = None
    company_id: str | None = None
    assignee_id: str | None = None


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    note: str | None = None
    due_date: datetime | None = None
    status: TaskStatus | None = None
    assignee_id: str | None = None


class TaskOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    note: str | None
    due_date: datetime | None
    status: TaskStatus
    company_id: str | None
    company_name: str | None = None
    assignee_id: str | None
    assignee_email: str | None = None
    overdue: bool = False
    created_at: datetime
