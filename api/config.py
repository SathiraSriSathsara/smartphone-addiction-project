"""Environment-backed application configuration."""

from functools import lru_cache
from pathlib import Path
from urllib.parse import urlsplit

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuration loaded from environment variables or a local `.env` file."""

    app_name: str = Field(default="SmartHabit API", validation_alias="APP_NAME")
    app_version: str = Field(default="1.0.0", validation_alias="APP_VERSION")
    environment: str = Field(default="development", validation_alias="ENVIRONMENT")
    model_path: Path = Field(
        default=Path("models/smartphone_addiction_model.joblib"),
        validation_alias="MODEL_PATH",
    )
    metadata_path: Path = Field(
        default=Path("models/model_metadata.json"),
        validation_alias="METADATA_PATH",
    )
    allowed_origins: str = Field(
        default="http://localhost:5500,http://127.0.0.1:5500",
        validation_alias="ALLOWED_ORIGINS",
    )
    max_request_body_bytes: int = Field(
        default=16_384,
        ge=1_024,
        le=1_048_576,
        validation_alias="MAX_REQUEST_BODY_BYTES",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def allowed_origins_list(self) -> list[str]:
        """Return non-empty CORS origins from the comma-separated setting."""
        return [
            origin.strip()
            for origin in self.allowed_origins.split(",")
            if origin.strip()
        ]

    @field_validator("allowed_origins")
    @classmethod
    def validate_allowed_origins(cls, value: str) -> str:
        """Reject wildcards and malformed origins before CORS is configured."""
        origins = [origin.strip() for origin in value.split(",") if origin.strip()]
        if not origins:
            raise ValueError("ALLOWED_ORIGINS must contain at least one origin")
        for origin in origins:
            parsed = urlsplit(origin)
            if (
                origin == "*"
                or parsed.scheme not in {"http", "https"}
                or not parsed.netloc
                or parsed.path not in {"", "/"}
                or parsed.query
                or parsed.fragment
            ):
                raise ValueError(
                    "ALLOWED_ORIGINS must contain explicit HTTP(S) origins"
                )
        return ",".join(origins)


@lru_cache
def get_settings() -> Settings:
    """Return one cached settings instance for the application process."""
    return Settings()
