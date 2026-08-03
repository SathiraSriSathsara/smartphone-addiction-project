"""FastAPI application factory and entry point."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from api.config import Settings, get_settings
from api.exceptions import register_exception_handlers
from api.logging_config import configure_logging
from api.middleware import RequestBodyLimitMiddleware, RequestContextMiddleware
from api.model_loader import ModelService
from api.routes.health import router as health_router
from api.routes.model import router as model_router
from api.routes.prediction import router as prediction_router


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create and configure the SmartHabit API and its startup model loader."""
    active_settings = settings or get_settings()
    configure_logging()

    @asynccontextmanager
    async def lifespan(application: FastAPI) -> AsyncIterator[None]:
        if not hasattr(application.state, "model_service"):
            environment_path = active_settings.metadata_path.parent / "environment.json"
            application.state.model_service = ModelService(
                model_path=active_settings.model_path,
                metadata_path=active_settings.metadata_path,
                environment_path=environment_path,
                schema_path=Path("docs/model-schema.json"),
            ).load()
        yield

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
        lifespan=lifespan,
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=active_settings.allowed_origins_list,
        allow_credentials=False,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["Accept", "Content-Type"],
    )
    application.add_middleware(
        RequestBodyLimitMiddleware,
        max_bytes=active_settings.max_request_body_bytes,
    )
    application.add_middleware(
        RequestContextMiddleware,
        environment=active_settings.environment,
    )
    register_exception_handlers(application)

    application.include_router(health_router)
    application.include_router(model_router)
    application.include_router(prediction_router)
    application.mount(
        "/",
        StaticFiles(directory=Path("web"), html=True),
        name="web",
    )
    return application


app = create_app()
