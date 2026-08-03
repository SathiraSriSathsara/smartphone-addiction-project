"""Tests for the API foundation endpoints."""

from datetime import datetime

from fastapi.testclient import TestClient

from api.config import get_settings


def test_root_endpoint_serves_landing_page(
    client: TestClient,
) -> None:
    """The single-port application serves the public landing page at root."""
    response = client.get("/")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    assert "Understand Today" in response.text
    assert "SmartHabit" in response.text


def test_health_endpoint_returns_status_and_timestamp(client: TestClient) -> None:
    """The health endpoint exposes required operational fields."""
    response = client.get("/api/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "healthy"
    assert payload["environment"] == get_settings().environment
    assert payload["version"] == get_settings().app_version
    parsed_timestamp = datetime.fromisoformat(payload["timestamp"])
    assert parsed_timestamp.tzinfo is not None


def test_unknown_route_uses_global_json_error_format(client: TestClient) -> None:
    """Framework-level HTTP errors use the common JSON envelope."""
    response = client.get("/not-a-route")

    assert response.status_code == 404
    assert response.json() == {
        "error": {
            "code": "http_error",
            "message": "Not Found",
        }
    }


def test_cors_allows_configured_origin(client: TestClient) -> None:
    """A configured local frontend origin receives a CORS allow header."""
    response = client.options(
        "/api/health",
        headers={
            "Origin": "http://localhost:5500",
            "Access-Control-Request-Method": "GET",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == (
        "http://localhost:5500"
    )
