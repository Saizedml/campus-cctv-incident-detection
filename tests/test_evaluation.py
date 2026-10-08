"""Synthetic tests for matching, uncertainty and camera-hour arithmetic."""

import math

import pytest

from campus_cctv.evaluation import (
    aggregate_metrics,
    evaluate,
    iomin,
    negative_hours,
    poisson_upper,
    wilson,
)


def event(identifier="event-a", onset=2.0, end=4.0, track=1):
    return {
        "event_id": identifier,
        "source_id": "synthetic-a",
        "camera_id": "camera-a",
        "task": "falls",
        "onset_s": onset,
        "end_s": end,
        "assigned_track_ids": [track],
    }


def alert(identifier="notice-a", time=2.0, kind="NEW", track=1):
    return {
        "alert_id": identifier,
        "source_id": "synthetic-a",
        "camera_id": "camera-a",
        "task": "falls",
        "decision_time_s": time,
        "kind": kind,
        "track_ids": [track],
    }


def test_one_notice_credits_one_event_and_updates_credit_recall():
    events = [event("first"), event("second")]
    notices = [alert("a"), alert("b", kind="UPDATE"), alert("c", time=3)]
    result = evaluate(events, notices, [])
    assert result["detected"] == 2
    assert result["matched"]["first"]["alert_id"] == "a"
    assert result["matched"]["second"]["alert_id"] == "b"
    assert result["duplicates"] == 1


def test_matching_window_closed_and_track_identity_required():
    assert evaluate([event()], [alert(time=1)], [])["detected"] == 1
    assert evaluate([event()], [alert(time=6)], [])["detected"] == 1
    assert evaluate([event()], [alert(time=6.001)], [])["detected"] == 0
    assert evaluate([event()], [alert(track=2)], [])["detected"] == 0


def test_only_new_counts_as_false_alert_and_exposure_is_half_open():
    notices = [alert("a", 1), alert("b", 2, "UPDATE"), alert("end", 3600)]
    result = evaluate([], notices, [{"source_id": "synthetic-a", "end_s": 3600}])
    assert result["false_alerts"] == 1
    assert result["fa_per_camera_hour"] == 1
    assert result["unmatched_alerts"] == 3


def test_exposure_union_subtracts_overlap_once_and_sums_cameras():
    exposures = [
        {"source_id": "synthetic-a", "end_s": 20},
        {"source_id": "synthetic-b", "end_s": 20},
    ]
    # Expanded intervals are [1, 6] and [3, 8]; their union is seven seconds.
    assert negative_hours(exposures, [event(), event("b", 4, 6)]) == 33 / 3600


def test_duplicates_are_not_false_alerts_or_extra_incidents():
    result = evaluate([event()], [alert("a"), alert("b", 3)], [])
    assert result["detected"] == 1
    assert result["duplicates"] == 1
    assert result["false_alerts"] == 0


def test_late_detection_reported_separately():
    result = evaluate([event(end=30)], [alert(time=15)], [])
    assert result["detected"] == 1
    assert result["detected_within_10s"] == 0
    assert result["late"] == 1
    assert result["delay_median_s"] == 13


def test_synchronised_weapon_localisation_uses_reference_coverage():
    truth = dict(event(), task="weapons", localisation="weapon_area_coverage")
    truth["reference_boxes"] = [{"time_s": 2, "box": [2, 2, 4, 4]}]
    notice = dict(alert(), task="weapons")
    notice["boxes"] = [{"time_s": 2, "box": [0, 0, 6, 6], "track_id": 1}]
    assert evaluate([truth], [notice], [])["detected"] == 1
    notice["boxes"][0]["time_s"] = 3
    assert evaluate([truth], [notice], [])["detected"] == 0
    assert iomin([0, 0, 0, 0], [0, 0, 6, 6]) == 0


def test_confidence_bounds_and_empty_denominator():
    assert wilson(0, 0) is None
    assert wilson(5, 10) == pytest.approx([0.236593090512564, 0.763406909487436])
    assert poisson_upper(0, 10) == pytest.approx(-math.log(0.05) / 10)
    with pytest.raises(ValueError):
        poisson_upper(1, 0)
    with pytest.raises(ValueError):
        wilson(11, 10)


def test_duplicate_ids_are_rejected_and_aggregate_output_removes_identifiers():
    with pytest.raises(ValueError, match="Event IDs"):
        evaluate([event(), event()], [], [])
    with pytest.raises(ValueError, match="Alert IDs"):
        evaluate([], [alert(), alert()], [])
    with pytest.raises(ValueError, match="distinct source"):
        negative_hours([{"source_id": "a", "end_s": 1}] * 2, [])
    result = aggregate_metrics(evaluate([event()], [alert()], []))
    assert "matched" not in result
    assert "duplicate_alert_ids" not in result
    assert result["detected"] == 1
