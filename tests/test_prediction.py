"""Prediction behavior and real-model integration tests."""

from collections.abc import Iterator
from typing import Any

import numpy as np
import pytest
from fastapi.testclient import TestClient

from api.dependencies import get_model_service
from api.main import app
from api.model_loader import ModelService
from api.predictor import risk_level_for_probability

VALID_INPUT = {
    "age": 24.0,
    "daily_screen_time_hours": 8.0,
    "social_media_hours": 2.5,
    "gaming_hours": 1.0,
    "work_study_hours": 3.0,
    "sleep_hours": 7.0,
    "notifications_per_day": 120.0,
    "app_opens_per_day": 90.0,
    "weekend_screen_time": 10.0,
    "gender": "Female",
    "stress_level": "Medium",
    "academic_work_impact": "No",
}


class ProbabilityModel:
    """Small binary estimator used to isolate response mapping behavior."""

    classes_ = np.asarray([0, 1])

    def __init__(self, addiction_probability: float) -> None:
        self.addiction_probability = addiction_probability

    def predict_proba(self, values: Any) -> np.ndarray:
        return np.asarray(
            [[1.0 - self.addiction_probability, self.addiction_probability]]
        )


def _prediction_service(addiction_probability: float) -> ModelService:
    service = ModelService.__new__(ModelService)
    service.model = ProbabilityModel(addiction_probability)
    service.metadata = {
        "feature_columns": [
            *VALID_INPUT.keys(),
            "social_media_ratio",
            "gaming_ratio",
            "notifications_per_screen_hour",
            "sleep_deficit_from_8h",
        ],
        "model_version": None,
    }
    service.schema = {"target": {"positive_class": 1}}
    return service


@pytest.fixture
def override_model_service() -> Iterator[None]:
    """Restore dependency overrides after each isolated prediction test."""
    yield
    app.dependency_overrides.pop(get_model_service, None)


@pytest.mark.usefixtures("override_model_service")
def test_valid_low_risk_input(client: TestClient) -> None:
    """A mocked low probability maps to the Low display band."""
    app.dependency_overrides[get_model_service] = lambda: _prediction_service(0.2)

    response = client.post("/api/predict", json=VALID_INPUT)

    assert response.status_code == 200
    assert response.json()["risk_level"] == "Low"
    assert response.json()["predicted_class"] == 0


@pytest.mark.usefixtures("override_model_service")
def test_valid_high_risk_input(client: TestClient) -> None:
    """A mocked high probability maps to the High display band."""
    app.dependency_overrides[get_model_service] = lambda: _prediction_service(0.8)

    response = client.post("/api/predict", json=VALID_INPUT)

    assert response.status_code == 200
    assert response.json()["risk_level"] == "High"
    assert response.json()["predicted_class"] == 1


def test_risk_threshold_boundaries() -> None:
    """Display bands implement the exact configured boundary semantics."""
    assert risk_level_for_probability(0.349999) == "Low"
    assert risk_level_for_probability(0.35) == "Moderate"
    assert risk_level_for_probability(0.649999) == "Moderate"
    assert risk_level_for_probability(0.65) == "High"


def test_real_model_prediction_response(client: TestClient) -> None:
    """A valid request runs through the real saved preprocessing/model pipeline."""
    response = client.post("/api/predict", json=VALID_INPUT)

    assert response.status_code == 200
    payload = response.json()
    assert set(payload) == {
        "predicted_class",
        "addiction_probability",
        "non_addiction_probability",
        "risk_level",
        "risk_message",
        "model_version",
        "disclaimer",
        "explanation",
    }
    assert 0.0 <= payload["addiction_probability"] <= 1.0
    assert 0.0 <= payload["non_addiction_probability"] <= 1.0
    assert payload["addiction_probability"] + payload["non_addiction_probability"] == (
        pytest.approx(1.0)
    )
    assert "educational" in payload["disclaimer"].lower()
    assert "not a medical" in payload["disclaimer"].lower()


@pytest.mark.usefixtures("override_model_service")
def test_unexpected_model_error_returns_safe_500(client: TestClient) -> None:
    """Model failures return the global safe envelope without internal details."""
    service = _prediction_service(0.5)

    def fail_prediction(values: Any) -> np.ndarray:
        raise RuntimeError("secret model path C:/private/model.joblib")

    service.model.predict_proba = fail_prediction
    app.dependency_overrides[get_model_service] = lambda: service

    with TestClient(app, raise_server_exceptions=False) as safe_client:
        response = safe_client.post("/api/predict", json=VALID_INPUT)

    assert response.status_code == 500
    assert response.json() == {
        "error": {
            "code": "internal_server_error",
            "message": "An unexpected server error occurred",
        }
    }
    assert "private" not in response.text.lower()
    assert "path" not in response.text.lower()
