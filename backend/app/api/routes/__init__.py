"""Agrège tous les routers de l'API v1."""
from fastapi import APIRouter

from app.api.routes import (
    auth,
    companies,
    documents,
    health,
    meta,
    offers,
    onboarding,
    reports,
    scores,
    users,
)

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(meta.router, prefix="/meta", tags=["meta"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(companies.router, prefix="/companies", tags=["companies"])
api_router.include_router(onboarding.router, tags=["onboarding"])
api_router.include_router(documents.router, tags=["documents"])
api_router.include_router(scores.router, tags=["readiness"])
api_router.include_router(reports.router, tags=["report"])
api_router.include_router(offers.router, tags=["offers"])
