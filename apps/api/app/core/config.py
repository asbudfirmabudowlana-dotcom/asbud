from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://buildsmart:buildsmart@localhost:5432/buildsmart"
    jwt_secret: str = "development-only-change-me"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    session_cookie_secure: bool = True
    two_factor_encryption_key: str | None = None
    smtp_host: str | None = None
    smtp_port: int = 587
    smtp_username: str | None = None
    smtp_password: str | None = None
    smtp_from_email: str | None = None
    smtp_use_tls: bool = True
    clamav_host: str | None = None
    clamav_port: int = 3310
    attachment_scanning_required: bool = True
    cors_origins: str = "http://localhost:3000"
    openai_api_key: str | None = None
    openai_model: str = "gpt-5.6-terra"
    stripe_secret_key: str | None = None
    stripe_webhook_secret: str | None = None
    stripe_price_basic_monthly: str | None = None
    stripe_price_basic_yearly: str | None = None
    stripe_price_professional_monthly: str | None = None
    stripe_price_professional_yearly: str | None = None
    # Zachowane dla zgodności z wcześniejszą konfiguracją: cena miesięczna.
    stripe_price_basic: str | None = None
    stripe_price_professional: str | None = None
    app_base_url: str = "http://localhost:8000"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
