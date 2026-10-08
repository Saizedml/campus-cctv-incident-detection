"""Offline dashboard tests use invented notices and no model or media files."""

import json

import pytest

from campus_cctv.dashboard import synthetic_notices, validate_notices, write_dashboard


def test_demo_is_synthetic_and_updates_keep_the_parent():
    notices = validate_notices(synthetic_notices())
    assert all(n["synthetic"] for n in notices)
    roots = {n["alert_id"] for n in notices if n["kind"] == "NEW"}
    assert all(n["parent_alert_id"] in roots for n in notices)
    assert {n["q"] for n in notices} == {2, 5}


def test_static_dashboard_has_no_network_dependency(tmp_path):
    html = write_dashboard(tmp_path).read_text()
    assert "/* DASHBOARD_STYLES */" not in html
    assert "/* DASHBOARD_SCRIPT */" not in html
    assert "SYNTHETIC_NOTICES" not in html
    assert "connect-src 'none'" in html
    assert "<script src=" not in html
    assert "Scores are model confidence, not probabilities." in html
    assert "Combined real-time test: not passed" in html
    assert "revised after the results were known (post-hoc)" in html
    assert "Revised ≤5, set before testing" in html
    assert "35.1" in html and "60.8" in html


def test_validation_rejects_duplicate_ids_and_invalid_confidence():
    notices = synthetic_notices()
    with pytest.raises(ValueError, match="unique"):
        validate_notices([notices[0], notices[0]])
    notices[0]["score"] = float("nan")
    with pytest.raises(ValueError, match="finite"):
        validate_notices(notices)
    notices[0]["score"] = 2
    with pytest.raises(ValueError, match="between"):
        validate_notices(notices)


def test_notice_interchange_is_plain_json():
    assert validate_notices(json.loads(json.dumps(synthetic_notices()))) == synthetic_notices()


def test_empty_import_rejected():
    with pytest.raises(ValueError, match="between one"):
        validate_notices([])
