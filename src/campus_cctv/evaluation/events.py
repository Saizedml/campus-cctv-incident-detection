"""Frozen event matching and negative camera-hour arithmetic.

The matching window is closed at onset minus one second and end plus two
seconds. One notice can credit at most one event; later qualifying notices
are duplicates. UPDATE notices can credit recall, but only NEW notices count
as false alerts. Localisation uses synchronised person evidence, not the
weapon detector box, unless a separate secondary analysis is requested.
"""

from __future__ import annotations

import math
from collections import defaultdict
from collections.abc import Mapping, Sequence
from typing import Any

import numpy as np
from scipy.stats import chi2

Record = Mapping[str, Any]


def iomin(a: Sequence[float], b: Sequence[float]) -> float:
    """Return intersection divided by the smaller non-negative box area."""
    area_a = max(0, a[2] - a[0]) * max(0, a[3] - a[1])
    area_b = max(0, b[2] - b[0]) * max(0, b[3] - b[1])
    intersection = max(0, min(a[2], b[2]) - max(a[0], b[0])) * max(
        0, min(a[3], b[3]) - max(a[1], b[1])
    )
    return intersection / min(area_a, area_b) if min(area_a, area_b) > 0 else 0.0


def coverage(reference: Sequence[float], candidate: Sequence[float]) -> float:
    """Return the fraction of a reference object covered by a person box."""
    area = max(0, reference[2] - reference[0]) * max(0, reference[3] - reference[1])
    intersection = max(0, min(reference[2], candidate[2]) - max(reference[0], candidate[0])) * max(
        0, min(reference[3], candidate[3]) - max(reference[1], candidate[1])
    )
    return intersection / area if area > 0 else 0.0


def localises(event: Record, alert: Record) -> bool:
    """Apply assigned-track or synchronised reference/person-box matching."""
    if event["task"] == "falls":
        return bool(set(event["assigned_track_ids"]) & set(alert["track_ids"]))
    references = event.get("reference_boxes", event.get("knife_boxes", []))
    for reference in references:
        for item in alert["boxes"]:
            if item["track_id"] not in alert["track_ids"]:
                continue
            if abs(reference["time_s"] - item["time_s"]) >= 1e-6:
                continue
            overlap = (
                coverage(reference["box"], item["box"])
                if event.get("localisation") == "weapon_area_coverage"
                else iomin(reference["box"], item["box"])
            )
            if overlap >= 0.5:
                return True
    return False


def poisson_upper(false_alerts: int, hours: float, confidence: float = 0.95) -> float:
    """Return the exact one-sided Poisson rate upper confidence bound."""
    if false_alerts < 0 or int(false_alerts) != false_alerts or hours <= 0:
        raise ValueError("A non-negative count and positive exposure are required")
    if not 0 < confidence < 1:
        raise ValueError("Confidence must be strictly between zero and one")
    return float(chi2.ppf(confidence, 2 * false_alerts + 2) / (2 * hours))


def wilson(successes: int, total: int) -> list[float] | None:
    """Return the two-sided Wilson 95% interval, or None for no events."""
    if not 0 <= successes <= total:
        raise ValueError("Require zero <= successes <= total")
    if not total:
        return None
    z = 1.959963984540054
    p = successes / total
    denominator = 1 + z * z / total
    centre = (p + z * z / (2 * total)) / denominator
    width = z * math.sqrt(p * (1 - p) / total + z * z / (4 * total * total)) / denominator
    return [max(0.0, centre - width), min(1.0, centre + width)]


def negative_hours(exposures: Sequence[Record], events: Sequence[Record]) -> float:
    """Subtract the union of expanded event intervals from each camera exposure.

    Inputs contain one non-overlapping recording interval per distinct source.
    Independent cameras contribute additively, including simultaneous recordings.
    """
    if len({e["source_id"] for e in exposures}) != len(exposures):
        raise ValueError("Use one exposure interval per distinct source")
    seconds = 0.0
    for exposure in exposures:
        start, end = exposure.get("start_s", 0.0), exposure["end_s"]
        if end <= start:
            raise ValueError("Exposure must have positive duration")
        intervals = sorted(
            (max(start, event["onset_s"] - 1), min(end, event["end_s"] + 2))
            for event in events
            if event["source_id"] == exposure["source_id"]
        )
        merged: list[list[float]] = []
        for a, b in intervals:
            if b <= a:
                continue
            if merged and a <= merged[-1][1]:
                merged[-1][1] = max(merged[-1][1], b)
            else:
                merged.append([a, b])
        seconds += end - start - sum(b - a for a, b in merged)
    return seconds / 3600


def evaluate(
    events: Sequence[Record], alerts: Sequence[Record], exposures: Sequence[Record]
) -> dict[str, Any]:
    """Score saved notices without models, threshold selection or relabelling.

    Events need IDs, source/camera/task, onset/end and localisation evidence.
    Alerts need IDs, source/camera/task, decision time, kind and track evidence.
    Exposures need source ID and start/end seconds. The output retains matching
    IDs for a private audit; publishing aggregate fields avoids event disclosure.
    """
    if len({event["event_id"] for event in events}) != len(events):
        raise ValueError("Event IDs must be unique")
    if len({alert["alert_id"] for alert in alerts}) != len(alerts):
        raise ValueError("Alert IDs must be unique")
    if any(alert.get("kind") not in {"NEW", "UPDATE"} for alert in alerts):
        raise ValueError("Each alert kind must be NEW or UPDATE")
    exposure_by_source = {e["source_id"]: e for e in exposures}
    if len(exposure_by_source) != len(exposures):
        raise ValueError("Use one exposure interval per distinct source")
    by_source: dict[tuple[str, str, str], list[Record]] = defaultdict(list)
    for event in events:
        by_source[event["source_id"], event["camera_id"], event["task"]].append(event)
    matched: dict[str, dict[str, Any]] = {}
    duplicates: list[str] = []
    unmatched: list[str] = []
    negative_false: list[str] = []
    for alert in sorted(alerts, key=lambda a: (a["decision_time_s"], a["alert_id"])):
        candidates = [
            event
            for event in by_source[alert["source_id"], alert["camera_id"], alert["task"]]
            if event["onset_s"] - 1 <= alert["decision_time_s"] <= event["end_s"] + 2
            and localises(event, alert)
        ]
        candidates.sort(key=lambda e: (e["event_id"] in matched, e["onset_s"], e["event_id"]))
        if candidates:
            event = candidates[0]
            if event["event_id"] in matched:
                duplicates.append(alert["alert_id"])
            else:
                matched[event["event_id"]] = {
                    "alert_id": alert["alert_id"],
                    "delay_s": alert["decision_time_s"] - event["onset_s"],
                }
        else:
            unmatched.append(alert["alert_id"])
            exposure = exposure_by_source.get(alert["source_id"])
            if (
                alert["kind"] == "NEW"
                and exposure
                and exposure.get("start_s", 0) <= alert["decision_time_s"] < exposure["end_s"]
            ):
                negative_false.append(alert["alert_id"])
    hours = negative_hours(exposures, events)
    ontime = sum(row["delay_s"] <= 10 for row in matched.values())
    delays = [row["delay_s"] for row in matched.values()]
    return {
        "events": len(events),
        "detected": len(matched),
        "detected_within_10s": ontime,
        "late": len(matched) - ontime,
        "missed": len(events) - len(matched),
        "missed_within_10s": len(events) - ontime,
        "duplicates": len(duplicates),
        "recall": len(matched) / len(events) if events else None,
        "recall_within_10s": ontime / len(events) if events else None,
        "wilson95": wilson(len(matched), len(events)),
        "wilson95_within_10s": wilson(ontime, len(events)),
        "unmatched_alerts": len(unmatched),
        "false_alerts": len(negative_false),
        "negative_camera_hours": hours,
        "fa_per_camera_hour": len(negative_false) / hours if hours > 0 else None,
        "fa_upper95": poisson_upper(len(negative_false), hours) if hours > 0 else None,
        "delay_median_s": float(np.median(delays)) if delays else None,
        "delay_p95_s": float(np.percentile(delays, 95)) if delays else None,
        "matched": matched,
        "duplicate_alert_ids": duplicates,
        "unmatched_alert_ids": unmatched,
        "negative_false_alert_ids": negative_false,
    }


def aggregate_metrics(result: Record) -> dict[str, Any]:
    """Remove event/notice identifiers while retaining numeric summary fields."""
    private_keys = {
        "matched",
        "duplicate_alert_ids",
        "unmatched_alert_ids",
        "negative_false_alert_ids",
    }
    return {key: value for key, value in result.items() if key not in private_keys}
