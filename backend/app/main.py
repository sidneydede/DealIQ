"""Point d'entrée FastAPI — DealIQ API."""
from __future__ import annotations

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes import api_router
from app.config import settings
from app.core.ratelimit import build_limiter

_DEFAULT_SECRET = "change-me-in-prod-please-use-a-long-random-value"

# Garde-fou : en production, refuser de démarrer avec le secret par défaut.
if settings.environment == "production" and settings.secret_key == _DEFAULT_SECRET:
    raise RuntimeError(
        "SECRET_KEY par défaut interdit en production — définissez une valeur forte."
    )

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

# Rate limiting sur les endpoints d'authentification (anti brute-force), actif en production.
_auth_limiter = build_limiter()
_RATE_LIMITED_PATHS = {
    f"{settings.api_v1_prefix}/auth/login",
    f"{settings.api_v1_prefix}/auth/register",
}

_SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "no-referrer",
    "X-XSS-Protection": "0",
}


@app.middleware("http")
async def security_and_ratelimit(request: Request, call_next):
    if settings.environment == "production" and request.url.path in _RATE_LIMITED_PATHS:
        ip = request.client.host if request.client else "unknown"
        if not _auth_limiter.allow(f"{ip}:{request.url.path}"):
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={"detail": "Trop de tentatives, réessayez plus tard."},
            )
    response = await call_next(request)
    for header, value in _SECURITY_HEADERS.items():
        response.headers[header] = value
    return response


app.include_router(api_router, prefix=settings.api_v1_prefix)


@app.get("/")
def root() -> dict:
    return {"app": settings.app_name, "docs": "/docs", "api": settings.api_v1_prefix}
