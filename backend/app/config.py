"""Settings loaded from the environment (12-factor style).

pydantic-settings reads each field from the matching env var, so the same code
runs locally (.env file) and on Railway (dashboard env vars) with no changes.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/jobboard"
    secret_key: str = "change-me"
    access_token_expire_hours: int = 12
    cors_origins: str = "http://localhost:5173"

    @property
    def cors_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


settings = Settings()
