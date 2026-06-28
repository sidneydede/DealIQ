"""Sonde de santé."""
from __future__ import annotations

from fastapi import APIRouter

from app.config import settings

router = APIRouter()


@router.get("/health")
def health() -> dict:
    return {"status": "ok", "app": settings.app_name, "env": settings.environment}
