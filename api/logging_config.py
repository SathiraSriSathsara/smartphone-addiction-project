"""Safe JSON logging for application-owned operational events."""

import json
import logging
from datetime import UTC, datetime


class JsonFormatter(logging.Formatter):
    """Render a small allow-listed set of log fields as one JSON object."""

    _FIELDS = (
        "request_id",
        "method",
        "path",
        "status_code",
        "duration_ms",
        "exception_type",
    )

    def format(self, record: logging.LogRecord) -> str:
        """Serialize a log record without request bodies or query strings."""
        payload: dict[str, object] = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        for field in self._FIELDS:
            value = getattr(record, field, None)
            if value is not None:
                payload[field] = value
        return json.dumps(payload, ensure_ascii=True, separators=(",", ":"))


def configure_logging() -> None:
    """Configure the SmartHabit logger once per process."""
    logger = logging.getLogger("smarthabit")
    if not any(getattr(handler, "_smarthabit_json", False) for handler in logger.handlers):
        handler = logging.StreamHandler()
        handler.setFormatter(JsonFormatter())
        handler._smarthabit_json = True  # type: ignore[attr-defined]
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False
