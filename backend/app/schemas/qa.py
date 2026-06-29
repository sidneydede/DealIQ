"""Schémas Pydantic — Q&A (M14)."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.domain.enums import QAStatus


class QuestionCreate(BaseModel):
    question: str = Field(min_length=3, max_length=4000)


class AnswerIn(BaseModel):
    answer: str = Field(min_length=1, max_length=4000)


class QAItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    interaction_id: str
    asked_by: str | None
    question: str
    answer: str | None
    answered_by: str | None
    status: QAStatus
    created_at: datetime
    updated_at: datetime
