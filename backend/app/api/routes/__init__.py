"""Agrège tous les routers de l'API v1."""
from fastapi import APIRouter

from app.api.routes import (
    admin,
    auth,
    cockpit,
    companies,
    documents,
    health,
    investors,
    kyc,
    matching,
    meta,
    offers,
    onboarding,
    qa,
    reporting,
    reports,
    scores,
    teasers,
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
api_router.include_router(cockpit.router, tags=["cockpit"])
api_router.include_router(reporting.router, tags=["reporting"])
api_router.include_router(admin.router, tags=["admin"])
api_router.include_router(investors.router, prefix="/investors", tags=["investors"])
api_router.include_router(matching.router, tags=["matching"])
api_router.include_router(teasers.router, tags=["teasers"])
api_router.include_router(qa.router, tags=["qa"])
api_router.include_router(kyc.router, tags=["kyc"])
