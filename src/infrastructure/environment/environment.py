from functools import lru_cache
from typing import Literal

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False
    )

    app_env: Literal["local", "test", "production"] = Field(
        default="local",
        alias="APP_ENV"
    )

    api_prefix: str = Field(
        default="/api/v1",
        alias="API_PREFIX"
    )

    redis_host: str = Field(
        default="redis",
        alias="REDIS_HOST"
    )

    redis_port: int = Field(
        default=6379,
        alias="REDIS_PORT"
    )

    redis_password: SecretStr | None = Field(
        default=None,
        alias="REDIS_PASSWORD"
    )

    session_cookie_name: str = Field(
        default="session_id",
        alias="SESSION_COOKIE_NAME"
    )

    session_cookie_secure: bool = Field(
        default=False,
        alias="SESSION_COOKIE_SECURE"
    )

    session_cookie_samesite: Literal["lax", "strict", "none"] = Field(
        default="lax",
        alias="SESSION_COOKIE_SAMESITE"
    )

    @field_validator("api_prefix")
    @classmethod
    def validate_api_prefix(cls, value: str) -> str:
        if not value.startswith("/"):
            raise ValueError("API_PREFIX must start with /")

        return value.rstrip("/")


@lru_cache
def get_environment() -> Environment:
    return Environment()