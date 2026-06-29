"""Schémas Pydantic — documents & checklist (M4)."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.domain.enums import DocumentStatus


class DocumentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    company_id: str
    doc_type: str
    filename: str
    content_type: str | None
    size_bytes: int | None
    sha256: str | None
    version: int
    status: DocumentStatus
    created_at: datetime


class DocumentStatusUpdate(BaseModel):
    status: DocumentStatus


class ChecklistItem(BaseModel):
    doc_type: str
    required: bool  # issu du doc_checklist du type de deal
    received: bool
    verified: bool
    documents: list[DocumentOut]
