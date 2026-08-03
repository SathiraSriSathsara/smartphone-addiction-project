"""Consistent JSON exception responses for the API."""

import logging
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger(__name__)


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
            exc.errors(),
        ),
    )


async def unexpected_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """Log unexpected errors and return a safe generic response."""
    logger.exception(
        "Unhandled API error for %s %s",
        request.method,
        request.url.path,
        exc_info=exc,
    )
    return JSONResponse(
        status_code=500,
        content=_error_payload(
            "internal_server_error",
            "An unexpected server error occurred",
        ),
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Register global handlers on a FastAPI application."""
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, unexpected_exception_handler)
