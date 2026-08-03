"""Request validation tests for the prediction API."""

import math

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from api.schemas import PredictionRequest
from tests.test_prediction import VALID_INPUT


def test_missing_required_field_returns_422(client: TestClient) -> None:
    """Every raw model input is required."""
    payload = dict(VALID_INPUT)
    payload.pop("sleep_hours")

    response = client.post("/api/predict", json=payload)

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "validation_error"


def test_invalid_category_returns_422(client: TestClient) -> None:
    """Categories outside the fitted encoder vocabulary are rejected."""
    payload = {**VALID_INPUT, "gender": "Unknown"}

    response = client.post("/api/predict", json=payload)

    assert response.status_code == 422


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("age", 17.0),
        ("daily_screen_time_hours", 24.0),
        ("notifications_per_day", -1.0),
        ("sleep_hours", 12.0),
    ],
)
def test_impossible_numeric_range_returns_422(
    client: TestClient,
    field: str,
    value: float,
) -> None:
    """Values outside observed dataset bounds are rejected."""
    response = client.post(
        "/api/predict",
        json={**VALID_INPUT, field: value},
    )

    assert response.status_code == 422


@pytest.mark.parametrize("invalid_value", [math.nan, math.inf, -math.inf])
def test_non_finite_numbers_are_rejected(invalid_value: float) -> None:
    """NaN and both infinities fail validation before DataFrame construction."""
    with pytest.raises(ValidationError):
        PredictionRequest(**{**VALID_INPUT, "age": invalid_value})


def test_extra_untrained_field_returns_422(client: TestClient) -> None:
    """The API rejects fields that were not part of the raw model contract."""
    response = client.post(
        "/api/predict",
        json={**VALID_INPUT, "id": 123},
    )

    assert response.status_code == 422
