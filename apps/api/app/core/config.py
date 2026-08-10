from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://buildsmart:buildsmart@localhost:5432/buildsmart"
    jwt_secret: str = "development-only-change-me"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 480
    cors_origins: str = "http://localhost:3000"
    openai_api_key: str | None = None
    openai_model: str = "gpt-5.6-terra"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
