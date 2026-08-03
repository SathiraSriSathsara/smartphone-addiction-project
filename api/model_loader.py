"""Validated, idempotent loading of trusted local model artifacts."""

import json
import logging
import platform
import threading
from importlib import metadata as importlib_metadata
from pathlib import Path
from typing import Any

import joblib

logger = logging.getLogger(__name__)


class ModelLoadError(RuntimeError):
    """Raised when trusted model artifacts cannot be loaded safely."""


class ModelService:
    """Own the single in-process model instance and its audited metadata."""

    _PACKAGE_NAMES = {
        "pandas": "pandas",
        "numpy": "numpy",
        "scikit_learn": "scikit-learn",
        "joblib": "joblib",
    }
    _STRICT_PACKAGES = {"scikit_learn", "joblib"}

    def __init__(
        self,
        model_path: Path,
        metadata_path: Path,
        environment_path: Path,
        schema_path: Path = Path("docs/model-schema.json"),
    ) -> None:
        """Configure trusted artifact locations without loading them yet."""
        self.model_path = model_path
        self.metadata_path = metadata_path
        self.environment_path = environment_path
        self.schema_path = schema_path
        self.model: Any | None = None
        self.metadata: dict[str, Any] = {}
        self.training_environment: dict[str, str] = {}
        self.schema: dict[str, Any] = {}
        self.version_warnings: list[str] = []
        self._load_lock = threading.Lock()

    @property
    def is_loaded(self) -> bool:
        """Report whether a validated model instance is available."""
        return self.model is not None

    def load(self) -> "ModelService":
        """Load and validate all artifacts exactly once for this service."""
        if self.is_loaded:
            return self

        with self._load_lock:
            if self.is_loaded:
                return self

            self._validate_required_files()
            metadata = self._read_json(self.metadata_path, "model metadata")
            environment = self._read_json(
                self.environment_path,
                "training environment",
            )
            schema = self._read_json(self.schema_path, "model schema")
            warnings = self.verify_runtime_versions(environment)

            try:
                model = joblib.load(self.model_path)
            except Exception as exc:
                raise ModelLoadError(
                    "The saved model could not be deserialized with the current "
                    "runtime. Verify the pinned model dependencies."
                ) from exc

            self._validate_model(model, metadata)
            self.model = model
            self.metadata = metadata
            self.training_environment = environment
            self.schema = schema
            self.version_warnings = warnings
            logger.info("Trusted smartphone-addiction model loaded successfully")
            return self

    def verify_runtime_versions(
        self,
        environment: dict[str, str],
    ) -> list[str]:
        """Validate pickle-critical versions and warn on other differences."""
        warnings: list[str] = []
        recorded_python = environment.get("python")
        runtime_python = platform.python_version()
        if recorded_python and recorded_python != runtime_python:
            warnings.append(
                f"Python version differs: trained with {recorded_python}, "
                f"running with {runtime_python}."
            )

        for environment_name, distribution_name in self._PACKAGE_NAMES.items():
            recorded = environment.get(environment_name)
            if not recorded:
                warnings.append(
                    f"Training version for {distribution_name} is not recorded."
                )
                continue
            try:
                runtime = importlib_metadata.version(distribution_name)
            except importlib_metadata.PackageNotFoundError as exc:
                raise ModelLoadError(
                    f"Required runtime package {distribution_name} is not installed."
                ) from exc

            if runtime == recorded:
                continue
            message = (
                f"{distribution_name} version mismatch: trained with {recorded}, "
                f"running with {runtime}."
            )
            if environment_name in self._STRICT_PACKAGES:
                raise ModelLoadError(
                    f"Unsafe model compatibility: {message}"
                )
            warnings.append(message)

        try:
            lightgbm_version = importlib_metadata.version("lightgbm")
        except importlib_metadata.PackageNotFoundError as exc:
            raise ModelLoadError(
                "Required runtime package lightgbm is not installed."
            ) from exc
        warnings.append(
            "The training LightGBM version is not recorded; "
            f"runtime version is {lightgbm_version}."
        )

        for warning in warnings:
            logger.warning("Model runtime compatibility warning: %s", warning)
        return warnings

    def safe_model_info(self) -> dict[str, Any]:
        """Return only metadata approved for the public model-info endpoint."""
        self._require_loaded()
        return {
            "model_name": self.metadata["selected_model"],
            "model_version": self.metadata.get("model_version"),
            "competition": self.metadata["competition"],
            "target": self.metadata["target_column"],
            "feature_count": len(self.metadata["feature_columns"]),
            "official_metric": self.metadata["official_metric"],
            "training_row_count": self.metadata["training_rows"],
        }

    def frontend_schema(self) -> dict[str, Any]:
        """Return the audited raw-input fields needed by the frontend."""
        self._require_loaded()
        return {
            "schema_version": self.schema["schema_version"],
            "fields": self.schema["input_fields"],
        }

    def _validate_required_files(self) -> None:
        missing = [
            path.name
            for path in (
                self.model_path,
                self.metadata_path,
                self.environment_path,
                self.schema_path,
            )
            if not path.is_file()
        ]
        if missing:
            raise ModelLoadError(
                "Required model artifact(s) are missing: " + ", ".join(missing)
            )

    @staticmethod
    def _read_json(path: Path, description: str) -> dict[str, Any]:
        try:
            content = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise ModelLoadError(f"Invalid or unreadable {description} file.") from exc
        if not isinstance(content, dict):
            raise ModelLoadError(f"The {description} file must contain a JSON object.")
        return content

    @staticmethod
    def _validate_model(model: Any, metadata: dict[str, Any]) -> None:
        for method_name in ("predict", "predict_proba"):
            if not callable(getattr(model, method_name, None)):
                raise ModelLoadError(
                    f"Loaded model does not support required method {method_name}."
                )

        required_metadata = {
            "selected_model",
            "competition",
            "target_column",
            "feature_columns",
            "official_metric",
            "training_rows",
        }
        missing_metadata = sorted(required_metadata.difference(metadata))
        if missing_metadata:
            raise ModelLoadError(
                "Model metadata is missing required field(s): "
                + ", ".join(missing_metadata)
            )

        expected_features = list(metadata["feature_columns"])
        loaded_features = list(getattr(model, "feature_names_in_", []))
        if loaded_features != expected_features:
            raise ModelLoadError(
                "Saved model feature names or order do not match model metadata."
            )

    def _require_loaded(self) -> None:
        if not self.is_loaded:
            raise ModelLoadError("The model service has not been loaded.")
