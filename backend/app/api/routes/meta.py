"""Endpoints de guidage produit (publics) : périmètre, notes pédagogiques, MVP."""

from fastapi import APIRouter

from app.config import settings
from app.domain.guidance import (
    MVP_SUCCESS_CRITERION,
    PEDAGOGICAL_NOTES,
    SCOPE,
)

router = APIRouter(prefix="/meta", tags=["meta"])


@router.get("")
def meta() -> dict:
    return {
        "app": settings.app_name,
        "version": "0.1.0",
        "mvp_success_criterion": MVP_SUCCESS_CRITERION,
        "scope": SCOPE,
    }


@router.get("/scope")
def scope() -> dict:
    return SCOPE


@router.get("/pedagogical-notes")
def pedagogical_notes() -> dict:
    return PEDAGOGICAL_NOTES
