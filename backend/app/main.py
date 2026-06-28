"""Point d'entrée FastAPI — DealIQ API."""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import api_router
from app.config import settings

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description=(
        "API DealIQ — qualification, préparation et mise en relation privée PME ↔ "
        "investisseurs qualifiés (UEMOA/CEMAC). Aucune offre au public, aucune garantie "
        "de financement."
    ),
    openapi_url=f"{settings.api_v1_prefix}/openapi.json",
    docs_url="/docs",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.api_v1_prefix)


@app.get("/")
def root() -> dict:
    return {"app": settings.app_name, "docs": "/docs", "api": settings.api_v1_prefix}
