"""Environment-backed application configuration."""

from functools import lru_cache
from pathlib import Path

from pydantic import Field
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


@lru_cache
def get_settings() -> Settings:
    """Return one cached settings instance for the application process."""
    return Settings()
