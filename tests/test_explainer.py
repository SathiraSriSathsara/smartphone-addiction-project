"""Tests for local LightGBM contribution explanations."""

from typing import Any

import pandas as pd

from api.explainer import EXPLANATION_LABEL, generate_local_explanation
from api.main import app
from src.feature_engineering import add_domain_features


VALID_ROW = {
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


def test_real_model_explanation_has_readable_top_factors(client: Any) -> None:
    """The real pipeline produces a bounded local explanation for one row."""
    del client
    service = app.state.model_service
    frame = add_domain_features(pd.DataFrame([VALID_ROW]))

    explanation = generate_local_explanation(service.model, frame)

    assert explanation.status == "available"
    assert explanation.label == EXPLANATION_LABEL
    assert 1 <= len(explanation.factors) <= 5
    assert max(factor.display_magnitude for factor in explanation.factors) == 100.0
    assert all(0.0 <= factor.display_magnitude <= 100.0 for factor in explanation.factors)
    assert all(
        factor.direction
        in {"increases_predicted_risk", "decreases_predicted_risk"}
        for factor in explanation.factors
    )
    assert all("numeric__" not in factor.feature for factor in explanation.factors)
    assert all("categorical__" not in factor.feature for factor in explanation.factors)
    assert "not percentages" in explanation.limitation


def test_prediction_response_contains_local_explanation(client: Any) -> None:
    """The public prediction response includes the structured explanation."""
    response = client.post("/api/predict", json=VALID_ROW)

    assert response.status_code == 200
    explanation = response.json()["explanation"]
    assert set(explanation) == {
        "status",
        "label",
        "method",
        "factors",
        "limitation",
        "message",
    }
    assert explanation["label"] == EXPLANATION_LABEL
    assert len(explanation["factors"]) <= 5


def test_explanation_failure_returns_non_blocking_fallback() -> None:
    """An incompatible pipeline returns an unavailable explanation safely."""
    explanation = generate_local_explanation(object(), pd.DataFrame([VALID_ROW]))

    assert explanation.status == "unavailable"
    assert explanation.factors == []
    assert explanation.method is None
    assert explanation.message is not None
    assert "prediction itself" in explanation.message
