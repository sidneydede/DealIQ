"""Configuration applicative (Pydantic settings, chargée depuis l'environnement / .env)."""
from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # App
    app_name: str = "DealIQ API"
    environment: str = "development"
    api_v1_prefix: str = "/api/v1"
    default_locale: str = "fr"
    default_currency: str = "XOF"

    # Base de données
    database_url: str = "postgresql+psycopg://dealiq:dealiq@localhost:5432/dealiq"

    # Sécurité / JWT
    secret_key: str = "change-me-in-prod-please-use-a-long-random-value"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 14

    # CORS (chaîne séparée par des virgules)
    cors_origins: str = "http://localhost:5173"

    # Stockage documentaire (mock S3 = système de fichiers local en MVP)
    storage_dir: str = "storage"
    max_upload_mb: int = 10

    # Rate limiting (appliqué aux endpoints sensibles ; actif en production)
    rate_limit_max: int = 10
    rate_limit_window_seconds: int = 60

    # IA / LLM (accélérateur ; mock par défaut, aucune clé requise)
    llm_provider: str = "mock"
    anthropic_api_key: str = ""

    # E-mail (notifications). Mock par défaut : aucun envoi réseau, juste journalisé.
    # Passer à "smtp" + renseigner smtp_* pour un envoi réel (SES SMTP, Resend, Mailgun, …).
    email_provider: str = "mock"  # mock | smtp
    email_from: str = "noreply@dealiq.com"
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    smtp_use_tls: bool = True

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
