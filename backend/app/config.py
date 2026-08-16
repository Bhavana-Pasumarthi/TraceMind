"""
Centralized application configuration.

All configuration is read from environment variables (see .env.example).
Nothing is hard-coded here — this is the single place the rest of the
codebase imports settings from, so there's one source of truth for how
the app is configured in dev, test, and (hypothetically) prod.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Environment
    environment: str = "development"
    log_level: str = "INFO"

    # Database
    database_url: str = "postgresql+psycopg://tracemind:tracemind@localhost:5432/tracemind"

    # Backend
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000

    # LLM provider abstraction (unused until Phase 9; kept here now so the
    # settings surface doesn't change shape mid-project)
    llm_provider: str = "none"
    llm_model: str | None = None
    llm_api_key: str | None = None

    # Simulator
    simulator_seed: int = 42


@lru_cache
def get_settings() -> Settings:
    """Cached settings accessor — avoids re-parsing env vars on every call."""
    return Settings()
