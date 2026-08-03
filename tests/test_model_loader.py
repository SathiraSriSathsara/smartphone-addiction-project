"""Tests for singleton model loading and public model routes."""

import json
from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient

from api.dependencies import get_model_service
from api.main import app
from api.model_loader import ModelLoadError, ModelService


class StubModel:
    """Minimal model object satisfying the loader contract."""

    feature_names_in_ = ["feature_a"]

    def predict(self, values: Any) -> list[int]:
        return [0]

    def predict_proba(self, values: Any) -> list[list[float]]:
        return [[0.75, 0.25]]


def _write_json(path: Path, content: dict[str, Any]) -> None:
    path.write_text(json.dumps(content), encoding="utf-8")


def _artifact_service(tmp_path: Path) -> ModelService:
    model_path = tmp_path / "model.joblib"
    metadata_path = tmp_path / "metadata.json"
    environment_path = tmp_path / "environment.json"
    schema_path = tmp_path / "schema.json"
    model_path.write_bytes(b"trusted-test-placeholder")
    _write_json(
        metadata_path,
        {
            "selected_model": "TestModel",
            "competition": "TestCompetition",
            "target_column": "target",
            "feature_columns": ["feature_a"],
            "official_metric": "roc_auc",
            "training_rows": 10,
        },
    )
    _write_json(
        environment_path,
        {
            "python": "0.0.0",
            "pandas": "0.0.0",
            "numpy": "0.0.0",
            "scikit_learn": "1.6.1",
            "joblib": "1.5.3",
        },
    )
    _write_json(
        schema_path,
        {"schema_version": "test", "input_fields": []},
    )
    return ModelService(
        model_path,
        metadata_path,
        environment_path,
        schema_path,
    )


def test_missing_model_file_fails_before_loading(tmp_path: Path) -> None:
    """Startup validation clearly identifies an absent required artifact."""
    service = ModelService(
        tmp_path / "missing-model.joblib",
        tmp_path / "missing-metadata.json",
        tmp_path / "missing-environment.json",
        tmp_path / "missing-schema.json",
    )

    with pytest.raises(ModelLoadError, match="Required model artifact"):
        service.load()


def test_unsafe_scikit_learn_mismatch_is_rejected(tmp_path: Path) -> None:
    """A pickle-critical scikit-learn mismatch prevents deserialization."""
    service = _artifact_service(tmp_path)
    environment = {
        "python": "0.0.0",
        "pandas": "0.0.0",
        "numpy": "0.0.0",
        "scikit_learn": "999.0.0",
        "joblib": "1.5.3",
    }

    with pytest.raises(ModelLoadError, match="Unsafe model compatibility"):
        service.verify_runtime_versions(environment)


def test_service_load_is_idempotent(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Repeated service access deserializes the model only once."""
    service = _artifact_service(tmp_path)
    load_calls = 0

    def fake_load(path: Path) -> StubModel:
        nonlocal load_calls
        load_calls += 1
        return StubModel()

    monkeypatch.setattr("api.model_loader.joblib.load", fake_load)

    assert service.load() is service
    assert service.load() is service
    assert load_calls == 1
    assert callable(service.model.predict)
    assert callable(service.model.predict_proba)


def test_real_saved_model_is_loaded_by_application(client: TestClient) -> None:
    """The application singleton contains the real compatible saved pipeline."""
    service = app.state.model_service

    assert service.is_loaded
    assert callable(service.model.predict)
    assert callable(service.model.predict_proba)
    assert len(service.model.feature_names_in_) == 16


def test_model_info_endpoint_exposes_only_safe_metadata(
    client: TestClient,
) -> None:
    """The info route contains the approved metadata fields and no paths."""
    response = client.get("/api/model/info")

    assert response.status_code == 200
    payload = response.json()
    assert set(payload) == {
        "model_name",
        "model_version",
        "competition",
        "target",
        "feature_count",
        "official_metric",
        "training_row_count",
    }
    assert payload["model_name"] == "LightGBM"
    assert payload["model_version"] is None
    assert payload["feature_count"] == 16
    assert "path" not in json.dumps(payload).lower()


def test_model_schema_endpoint_returns_frontend_fields(client: TestClient) -> None:
    """The schema route exposes all audited raw inputs and category choices."""
    response = client.get("/api/model/schema")

    assert response.status_code == 200
    payload = response.json()
    assert payload["schema_version"] == "1.0.0"
    assert len(payload["fields"]) == 12
    gender = next(field for field in payload["fields"] if field["name"] == "gender")
    assert gender == {
        "name": "gender",
        "type": "string",
        "required": True,
        "allowed_categories": ["Female", "Male", "Other"],
    }
