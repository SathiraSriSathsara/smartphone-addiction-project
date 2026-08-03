"""Consistent JSON exception responses for the API."""

import logging
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger("smarthabit.error")


def _safe_error_headers(request: Request) -> dict[str, str]:
    """Return headers that must survive framework-level 500 handling."""
    return {
        "X-Request-ID": getattr(request.state, "request_id", "unavailable"),
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "Referrer-Policy": "no-referrer",
        "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
        "Cache-Control": "no-store",
    }


def _error_payload(
    code: str,
    message: str,
    details: Any | None = None,
) -> dict[str, dict[str, Any]]:
    """Build the public error response envelope."""
    error: dict[str, Any] = {"code": code, "message": message}
    if details is not None:
        error["details"] = details
    return {"error": error}


def _safe_validation_details(exc: RequestValidationError) -> list[dict[str, Any]]:
    """Expose actionable validation fields without echoing submitted values."""
    return [
        {
            "loc": list(error.get("loc", ())),
            "msg": error.get("msg", "Invalid value"),
            "type": error.get("type", "value_error"),
        }
        for error in exc.errors()
    ]


async def http_exception_handler(
    request: Request,
    exc: StarletteHTTPException,
) -> JSONResponse:
    """Convert HTTP errors, including 404 responses, to the common format."""
    del request
    message = exc.detail if isinstance(exc.detail, str) else "Request failed"
    details = None if isinstance(exc.detail, str) else exc.detail
    return JSONResponse(
        status_code=exc.status_code,
        content=_error_payload("http_error", message, details),
        headers=exc.headers,
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    """Return request validation failures without exposing internal details."""
    del request
    return JSONResponse(
        status_code=422,
        content=_error_payload(
            "validation_error",
            "Request validation failed",
            _safe_validation_details(exc),
        ),
    )


async def unexpected_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """Log unexpected errors and return a safe generic response."""
    logger.error(
        "unhandled_exception",
        extra={
            "request_id": getattr(request.state, "request_id", "unavailable"),
            "method": request.method,
            "path": request.url.path,
            "status_code": 500,
            "exception_type": type(exc).__name__,
        },
    )
    return JSONResponse(
        status_code=500,
        content=_error_payload(
            "internal_server_error",
            "An unexpected server error occurred",
        ),
        headers=_safe_error_headers(request),
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Register global handlers on a FastAPI application."""
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, unexpected_exception_handler)
