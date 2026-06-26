from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuration applicative chargée depuis l'environnement / .env."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Méta
    app_name: str = "DealIQ"
    environment: str = "dev"

    # Base de données
    database_url: str = "postgresql+psycopg2://dealiq:dealiq@localhost:5432/dealiq"
    redis_url: str = "redis://localhost:6379/0"

    # Sécurité / Auth
    secret_key: str = "change-me-in-prod"
    access_token_expire_minutes: int = 480
    jwt_algorithm: str = "HS256"

    # Premier utilisateur (créé au seed)
    first_user_email: str = "analyste@dealiq.ci"
    first_user_password: str = "changeme"

    # Enrichissement (Phase 2) — aucune clé pour l'instant
    enrichment_mode: str = "mock"  # mock | live
    x_bearer_token: str = ""
    crunchbase_api_key: str = ""
    anthropic_api_key: str = ""


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
