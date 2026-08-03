"""Application health endpoint."""

from datetime import UTC, datetime

from fastapi import APIRouter, Depends

from api.config import Settings, get_settings

router = APIRouter(prefix="/api", tags=["Health"])


@router.get(
    "/health",
    summary="Check application health",
    description="Reports API availability without loading or checking the ML model.",
)
def health_check(settings: Settings = Depends(get_settings)) -> dict[str, str]:
    """Return current API status and non-sensitive runtime metadata."""
    return {
        "status": "healthy",
        "environment": settings.environment,
        "version": settings.app_version,
        "timestamp": datetime.now(UTC).isoformat(),
    }
