"""Validated smartphone-addiction prediction route."""

from fastapi import APIRouter, Depends

from api.dependencies import get_model_service
from api.model_loader import ModelService
from api.predictor import predict_addiction
from api.schemas import PredictionRequest, PredictionResponse

router = APIRouter(prefix="/api", tags=["Prediction"])


@router.post(
    "/predict",
    response_model=PredictionResponse,
    summary="Predict smartphone-addiction likelihood",
    description=(
        "Returns an educational model estimate. This is not a medical or "
        "psychological diagnosis. When available, up to five local TreeSHAP "
        "model influences are returned as non-causal directional factors."
    ),
)
def predict(
    request: PredictionRequest,
    service: ModelService = Depends(get_model_service),
) -> PredictionResponse:
    """Run one validated request through feature engineering and the pipeline."""
    return predict_addiction(request, service)
