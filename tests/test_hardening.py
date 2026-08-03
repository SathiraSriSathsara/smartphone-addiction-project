"""Security and reliability middleware regression tests."""

import json
from uuid import UUID

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from api.config import Settings
from tests.test_prediction import VALID_INPUT


def test_response_has_request_id_and_security_headers(client: TestClient) -> None:
    response = client.get("/api/health")

    UUID(response.headers["x-request-id"])
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["x-frame-options"] == "DENY"
    assert response.headers["referrer-policy"] == "no-referrer"
    assert response.headers["cache-control"] == "no-store"
    assert "camera=()" in response.headers["permissions-policy"]


def test_oversized_request_is_rejected(client: TestClient) -> None:
    oversized = json.dumps({**VALID_INPUT, "padding": "x" * 20_000})
    response = client.post(
        "/api/predict",
        content=oversized,
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 413
    assert response.json()["error"]["code"] == "request_too_large"
    UUID(response.headers["x-request-id"])


def test_validation_response_does_not_echo_input(client: TestClient) -> None:
    private_value = "do-not-echo-this-value"
    response = client.post(
        "/api/predict",
        json={**VALID_INPUT, "gender": private_value},
    )

    assert response.status_code == 422
    assert private_value not in response.text
    detail = response.json()["error"]["details"][0]
    assert set(detail) == {"loc", "msg", "type"}


@pytest.mark.parametrize("origins", ["*", "file:///tmp/frontend", "https://example.com/path"])
def test_cors_rejects_unsafe_origins(origins: str) -> None:
    with pytest.raises(ValidationError):
        Settings(ALLOWED_ORIGINS=origins)
