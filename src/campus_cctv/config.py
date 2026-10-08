"""Load portable runtime configuration without downloading models or data."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
from typing import Any

import yaml

TIERS = {"Alert now": "2.0", "Check when free": "5.0"}


def operating_point(value: str | float) -> str:
    """Resolve a tier or one of the six frozen validation-budget labels."""
    if value in TIERS:
        return TIERS[value]
    try:
        number = float(value)
    except (ValueError, TypeError) as exc:
        raise ValueError(f"Unknown operating point: {value}") from exc
    if number not in (0.1, 0.25, 0.5, 1, 2, 5):
        raise ValueError(f"Operating point must be one of the six frozen budgets: {value}")
    return str(number)


def load_config(path: str | Path) -> dict[str, Any]:
    """Load YAML; expand environment variables and reject unresolved values."""
    source = Path(path)
    if not source.is_file():
        raise FileNotFoundError("Configuration is missing; supply a readable YAML file.")
    result = yaml.safe_load(source.read_text(encoding="utf-8"))
    if not isinstance(result, dict):
        raise ValueError("Configuration must be a YAML mapping.")

    def expand(value: Any) -> Any:
        if isinstance(value, str):
            value = os.path.expandvars(value)
            if "${" in value or value.startswith("$"):
                raise ValueError("A configuration environment variable is unset.")
            return value
        if isinstance(value, dict):
            return {str(k): expand(v) for k, v in value.items()}
        if isinstance(value, list):
            return [expand(item) for item in value]
        return value

    return expand(result)


def require_weights(path: str | Path, sha256: str | None = None) -> Path:
    """Require locally supplied weights and optionally verify their exact digest."""
    result = Path(path).expanduser()
    if not result.is_file():
        raise FileNotFoundError(
            "Model weights are not included. Supply an authorised local checkpoint "
            "using the weights setting; see docs/data.md."
        )
    if sha256:
        with result.open("rb") as stream:
            actual = hashlib.file_digest(stream, "sha256").hexdigest()
        if actual != sha256:
            raise ValueError("Checkpoint digest does not match the frozen model contract.")
    return result
