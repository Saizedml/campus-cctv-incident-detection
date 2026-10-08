"""Offline review dashboard with synthetic demonstration evidence."""

from __future__ import annotations

import json
from importlib.resources import files
from pathlib import Path
from typing import Any


def synthetic_notices() -> list[dict[str, Any]]:
    """Return invented notices for interface demonstration, never evaluation."""
    return [
        {
            "alert_id": "demo-weapon-a",
            "parent_alert_id": "demo-weapon-a",
            "kind": "NEW",
            "task": "weapons",
            "q": 2,
            "source_id": "Illustrated walkway",
            "decision_time_s": 12.5,
            "score": 0.87,
            "track_id": 1,
            "synthetic": True,
        },
        {
            "alert_id": "demo-weapon-a-update",
            "parent_alert_id": "demo-weapon-a",
            "kind": "UPDATE",
            "task": "weapons",
            "q": 2,
            "source_id": "Illustrated walkway",
            "decision_time_s": 14.0,
            "score": 0.89,
            "track_id": 1,
            "synthetic": True,
        },
        {
            "alert_id": "demo-falls-a",
            "parent_alert_id": "demo-falls-a",
            "kind": "NEW",
            "task": "falls",
            "q": 2,
            "source_id": "Illustrated courtyard",
            "decision_time_s": 26.0,
            "score": 0.73,
            "track_id": 2,
            "synthetic": True,
        },
        {
            "alert_id": "demo-weapon-b",
            "parent_alert_id": "demo-weapon-b",
            "kind": "NEW",
            "task": "weapons",
            "q": 5,
            "source_id": "Illustrated entrance",
            "decision_time_s": 31.0,
            "score": 0.42,
            "track_id": 3,
            "synthetic": True,
        },
        {
            "alert_id": "demo-falls-b",
            "parent_alert_id": "demo-falls-b",
            "kind": "NEW",
            "task": "falls",
            "q": 5,
            "source_id": "Illustrated courtyard",
            "decision_time_s": 38.0,
            "score": 0.48,
            "track_id": 4,
            "synthetic": True,
        },
    ]


def validate_notices(notices: Any) -> list[dict[str, Any]]:
    """Validate the dashboard's small, media-free notice interchange format."""
    if not isinstance(notices, list) or not 1 <= len(notices) <= 10000:
        raise ValueError("Supply a list containing between one and 10,000 notices")
    seen: set[str] = set()
    for notice in notices:
        if not isinstance(notice, dict):
            raise ValueError("Each notice must be an object")
        for key in ("alert_id", "parent_alert_id", "source_id"):
            if not isinstance(notice.get(key), str) or not notice[key]:
                raise ValueError(f"Each notice needs a non-empty {key}")
        if notice["alert_id"] in seen:
            raise ValueError("Notice IDs must be unique")
        seen.add(notice["alert_id"])
        if notice.get("kind") not in {"NEW", "UPDATE"}:
            raise ValueError("Notice kind must be NEW or UPDATE")
        if notice.get("task") not in {"weapons", "falls"}:
            raise ValueError("Notice task must be weapons or falls")
        if notice.get("q") not in {2, 5}:
            raise ValueError("Only the two dashboard tiers are supported")
        for key in ("decision_time_s", "score"):
            value = notice.get(key)
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                raise ValueError(f"Notice {key} must be a finite non-negative number")
            if not 0 <= value < float("inf"):
                raise ValueError(f"Notice {key} must be a finite non-negative number")
        if notice["score"] > 1:
            raise ValueError("Model confidence must lie between zero and one")
    return notices


def write_dashboard(directory: Path) -> Path:
    """Write a self-contained local HTML dashboard and return its path."""
    resource = files(__package__).joinpath("static")
    html = resource.joinpath("index.html").read_text(encoding="utf-8")
    html = html.replace(
        "/* DASHBOARD_STYLES */", resource.joinpath("styles.css").read_text(encoding="utf-8")
    )
    html = html.replace(
        "/* DASHBOARD_SCRIPT */", resource.joinpath("app.js").read_text(encoding="utf-8")
    )
    payload = json.dumps(validate_notices(synthetic_notices()), allow_nan=False).replace(
        "</", "<\\/"
    )
    html = html.replace("SYNTHETIC_NOTICES", payload)
    directory.mkdir(parents=True, exist_ok=True)
    target = directory / "index.html"
    target.write_text(html, encoding="utf-8")
    return target
