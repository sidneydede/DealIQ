from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import auth, health
from app.config import settings

app = FastAPI(
    title=settings.app_name,
    description="Sourcing manuel + enrichissement assisté de deals VC (CI/UEMOA)",
    version="0.1.0",
)

# CORS : front Vite en dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api")
app.include_router(auth.router, prefix="/api")


@app.get("/")
def root() -> dict:
    return {"app": settings.app_name, "docs": "/docs"}
