"""Read-only public model metadata routes."""

from typing import Any

from fastapi import APIRouter, Depends

from api.dependencies import get_model_service
from api.model_loader import ModelService

router = APIRouter(prefix="/api/model", tags=["Model"])


@router.get(
    "/info",
    summary="Get safe model information",
    description="Returns non-sensitive metadata about the loaded educational model.",
)
def model_info(
    service: ModelService = Depends(get_model_service),
) -> dict[str, Any]:
    """Return the public subset of saved model metadata."""
    return service.safe_model_info()


@router.get(
    "/schema",
    summary="Get prediction input schema",
    description="Returns the audited raw fields required by the frontend.",
)
def model_schema(
    service: ModelService = Depends(get_model_service),
) -> dict[str, Any]:
    """Return input names, types, required flags, and allowed categories."""
    return service.frontend_schema()
