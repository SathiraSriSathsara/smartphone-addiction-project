"""FastAPI dependencies for shared application services."""

from fastapi import HTTPException, Request, status

from api.model_loader import ModelService


def get_model_service(request: Request) -> ModelService:
    """Return the application singleton or a safe service-unavailable error."""
    service = getattr(request.app.state, "model_service", None)
    if not isinstance(service, ModelService) or not service.is_loaded:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model service is unavailable",
        )
    return service
