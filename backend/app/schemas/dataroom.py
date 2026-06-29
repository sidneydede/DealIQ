"""Schémas Pydantic — data room (M13)."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.domain.enums import DataRoomLogAction, DataRoomStatus


class DataRoomOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    company_id: str
    provider_ref: str | None
    status: DataRoomStatus
    created_at: datetime


class AddDocumentIn(BaseModel):
    document_id: str


class DataRoomDocumentOut(BaseModel):
    id: str  # id de la liaison DataRoomDocument
    document_id: str
    filename: str
    doc_type: str
    status: str


class GrantAccessIn(BaseModel):
    investor_id: str
    expires_at: datetime | None = None


class DataRoomAccessOut(BaseModel):
    id: str
    investor_id: str
    investor_name: str | None
    granted_by: str | None
    expires_at: datetime | None
    revoked: bool
    created_at: datetime


class DataRoomLogOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    document_id: str | None
    investor_id: str | None
    actor_id: str | None
    action: DataRoomLogAction
    created_at: datetime


class DocumentViewOut(BaseModel):
    document_id: str
    filename: str
    watermark: str
    view_url: str  # URL mock (proxy VDR achetée à brancher)
    note: str
