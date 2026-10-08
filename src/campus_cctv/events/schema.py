"""Small, explicit notice contracts used before evidence is packaged."""

from __future__ import annotations

import math
from collections.abc import Sequence
from typing import Any, Literal, TypedDict


class TrackEvidence(TypedDict):
    """One source-time person box supporting event localisation."""

    time_s: float
    track_id: int
    box: list[float]


class Notice(TypedDict):
    """Immediate decision metadata; movie evidence is packaged separately."""

    alert_id: str
    source_id: str
    camera_id: str
    task: Literal["weapons", "falls"]
    time_s: float
    decision_time_s: float
    frame_index: int
    track_id: int
    track_ids: list[int]
    boxes: list[TrackEvidence]
    kind: Literal["NEW", "UPDATE"]
    score: float
    q: str


def box_iou(a: Sequence[float], b: Sequence[float]) -> float:
    """Intersection over union for two continuous xyxy boxes."""
    intersection = max(0.0, min(a[2], b[2]) - max(a[0], b[0])) * max(
        0.0, min(a[3], b[3]) - max(a[1], b[1])
    )
    union = (
        max(0.0, a[2] - a[0]) * max(0.0, a[3] - a[1])
        + max(0.0, b[2] - b[0]) * max(0.0, b[3] - b[1])
        - intersection
    )
    return intersection / union if union > 0 else 0.0


def validate_notice(notice: dict[str, Any]) -> None:
    """Reject malformed decisions; a confidence is never a probability claim."""
    for field in ("source_id", "task", "time_s", "track_id", "kind", "score", "q"):
        if field not in notice:
            raise ValueError(f"Notice is missing {field}")
    if notice["task"] not in {"weapons", "falls"}:
        raise ValueError("Unknown task")
    if notice["kind"] not in {"NEW", "UPDATE"}:
        raise ValueError("Notice kind must be NEW or UPDATE")
    if not math.isfinite(notice["time_s"]) or notice["time_s"] < 0:
        raise ValueError("Decision time must be finite and non-negative")
    if not math.isfinite(notice["score"]) or not 0 <= notice["score"] <= 1:
        raise ValueError("Confidence must lie in [0, 1]")


def notice_record(
    notice: dict[str, Any],
    *,
    source_id: str,
    camera_id: str,
    frame_index: int,
    serial: int,
    tracks: list[dict[str, Any]],
) -> dict[str, Any]:
    """Add evaluator identity and current-box evidence without changing a decision."""
    result = dict(notice)
    track = next(item for item in tracks if item["track_id"] == notice["track_id"])
    result.update(
        source_id=source_id,
        camera_id=camera_id,
        frame_index=frame_index,
        alert_id=f"{source_id}:notice:{serial:09d}",
        decision_time_s=notice["time_s"],
        track_ids=[notice["track_id"]],
        boxes=[dict(time_s=notice["time_s"], track_id=notice["track_id"], box=list(track["box"]))],
    )
    validate_notice(result)
    return result
