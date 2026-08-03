"""FastAPI application factory and entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.config import Settings, get_settings
from api.exceptions import register_exception_handlers
from api.routes.health import router as health_router


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create and configure the SmartHabit API without loading the ML model."""
    active_settings = settings or get_settings()
    application = FastAPI(
        title=active_settings.app_name,
        version=active_settings.app_version,
        description=(
            "Educational smartphone-addiction prediction API foundation. "
            "This prototype does not provide a medical or psychological diagnosis."
        ),
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        contact={"name": "SmartHabit Project"},
        license_info={"name": "Educational use"},
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=active_settings.allowed_origins_list,
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["Accept", "Authorization", "Content-Type"],
    )
    register_exception_handlers(application)

    @application.get(
        "/",
        tags=["Application"],
        summary="Get application information",
    )
    def root() -> dict[str, str]:
        """Return public application metadata and the Swagger UI path."""
        return {
            "name": active_settings.app_name,
            "version": active_settings.app_version,
            "docs_url": application.docs_url or "/docs",
        }

    application.include_router(health_router)
    return application


app = create_app()
