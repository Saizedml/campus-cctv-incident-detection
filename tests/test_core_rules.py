"""Synthetic boundaries for frozen decisions; no models or datasets are used."""

from pathlib import Path

import pytest

from campus_cctv.config import load_config, operating_point, require_weights
from campus_cctv.falls.rules import FallsRule, FallsRuntime
from campus_cctv.weapons.rules import WeaponRule, WeaponRuntime
from campus_cctv.weapons.verifier import allowed_tokens, select_evidence

BOX = [20, 20, 60, 90]


def rule() -> WeaponRule:
    """Return synthetic thresholds that exercise both cascade branches."""
    return WeaponRule(tau_a=0.2, tau_hi=0.6, veto_hi=0.6)


def track(tid: int = 1, box: list | None = None) -> dict:
    """Construct one synthetic person box."""
    return {"track_id": tid, "box": box or BOX}


def test_veto_only_below_high_threshold() -> None:
    runtime = WeaponRuntime(rule())
    assert runtime.process(0, [track()], {1: 0.59}, verdict=lambda *_: "not_weapon") == []
    notices = runtime.process(
        0.5, [track()], {1: 0.6}, verdict=lambda *_: pytest.fail("V must be bypassed")
    )
    assert notices[0]["kind"] == "NEW"
    assert notices[0]["high_pass"] is True


def test_veto_does_not_consume_cooldown_and_uncertain_passes() -> None:
    runtime = WeaponRuntime(rule())
    assert runtime.process(0, [track()], {1: 0.3}, verdict=lambda *_: "not_weapon") == []
    assert (
        runtime.process(0.5, [track()], {1: 0.3}, verdict=lambda *_: "uncertain")[0]["kind"]
        == "NEW"
    )


def test_required_verifier_answer_is_not_silently_missing() -> None:
    with pytest.raises(ValueError, match="requires a verifier"):
        WeaponRuntime(rule()).process(0, [track()], {1: 0.3})


def test_cooldown_is_60_seconds_from_new_not_last_update() -> None:
    runtime = WeaponRuntime(rule())
    kinds = [runtime.process(now, [track()], {1: 0.9})[0]["kind"] for now in [0, 1, 59.999, 60, 61]]
    assert kinds == ["NEW", "UPDATE", "UPDATE", "NEW", "UPDATE"]


def test_changed_id_attaches_by_recent_person_overlap() -> None:
    runtime = WeaponRuntime(rule())
    first = runtime.process(0, [track()], {1: 0.9})[0]
    second = runtime.process(2, [track(2)], {2: 0.9})[0]
    assert second["kind"] == "UPDATE"
    assert second["parent"] == first["parent"]
    assert runtime.process(4.1, [track(3)], {3: 0.9})[0]["kind"] == "NEW"


def test_window_is_open_on_left_boundary() -> None:
    runtime = WeaponRuntime(rule())
    assert runtime.process(0, [track()], {1: 0.9})
    assert runtime.process(2, [track()], {}) == []


def test_falls_down_persists_half_second_or_peak() -> None:
    runtime = FallsRuntime(FallsRule())
    assert all(runtime.process(t / 10, 1, 0.1, 0.35, box=BOX, height=200) is None for t in range(5))
    notice = runtime.process(0.5, 1, 0.1, 0.35, box=BOX, height=200)
    assert notice["reason"] == 1
    peak = runtime.process(0.6, 2, 0.95, 0.0, box=BOX, height=200)
    assert peak["reason"] == 4


def test_falls_120_seconds_and_gap_breaks_down_persistence() -> None:
    runtime = FallsRuntime(FallsRule())
    assert runtime.process(0, 1, 0.95, 0, box=BOX, height=200)["kind"] == "NEW"
    assert runtime.process(119.9, 1, 0.95, 0, box=BOX, height=200)["kind"] == "UPDATE"
    assert runtime.process(120, 1, 0.95, 0, box=BOX, height=200)["kind"] == "NEW"
    other = FallsRuntime(FallsRule())
    assert other.process(0, 1, 0, 0.9, box=BOX, height=200) is None
    assert other.process(0.5, 1, 0, 0.9, box=BOX, height=200) is None


def test_border_veto_keeps_rule_state_but_does_not_open_alert() -> None:
    runtime = FallsRuntime(FallsRule(B="on"))
    assert runtime.process(0, 1, 1, 0, box=[20, 0, 60, 90], height=200) is None
    assert runtime.process(1, 1, 1, 0, box=BOX, height=200) is None
    assert runtime.process(1.1, 1, 1, 0, box=BOX, height=200)["kind"] == "NEW"


def test_operating_points_and_frozen_tiers() -> None:
    assert operating_point("Alert now") == "2.0"
    assert operating_point("Check when free") == "5.0"
    assert operating_point(0.25) == "0.25"
    with pytest.raises(ValueError):
        operating_point(3)
    root = Path(__file__).resolve().parents[1]
    weapons = load_config(root / "configs/weapons.yaml")
    falls = load_config(root / "configs/falls.yaml")
    assert len(weapons["operating_points"]) == len(falls["operating_points"]) == 6
    assert (
        weapons["operating_points"]["1.0"]["tau_a"] == weapons["operating_points"]["2.0"]["tau_a"]
    )
    assert falls["operating_points"]["2.0"]["B"] == "off"


def test_config_environment_and_missing_input(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    config = tmp_path / "runtime.yaml"
    config.write_text("weights: ${CCTV_TEST_WEIGHTS}\n", encoding="utf-8")
    monkeypatch.delenv("CCTV_TEST_WEIGHTS", raising=False)
    with pytest.raises(ValueError, match="unset"):
        load_config(config)
    monkeypatch.setenv("CCTV_TEST_WEIGHTS", "local-model.pt")
    assert load_config(config)["weights"] == "local-model.pt"
    with pytest.raises(FileNotFoundError, match="not included"):
        require_weights(tmp_path / "absent.pt")


def test_causal_evidence_and_constrained_answers() -> None:
    def row(time: float, score: float) -> dict:
        return dict(
            time_s=time,
            frame_index=int(time * 10),
            detections=[
                dict(
                    name="knife",
                    track_id=1,
                    score=score,
                    crop_box=[0, 0, 10, 10],
                )
            ],
        )

    selected = select_evidence([row(0, 0.5), row(1, 0.9), row(2, 1.0)], 1, 1)
    assert [item["time_s"] for item in selected] == [1, 0, 0]
    assert allowed_tokens([[1, 2], [1, 3]], 9, [1]) == [2, 3]
    assert allowed_tokens([[1, 2], [1, 3]], 9, [1, 2]) == [9]


def test_notice_representation_preserves_frozen_decision() -> None:
    from campus_cctv.events.schema import notice_record

    runtime = WeaponRuntime(rule())
    fields = ("q", "task", "time_s", "track_id", "kind", "parent", "score")
    for serial, at in enumerate((0, 1)):
        original = runtime.process(at, [track()], {1: 0.9})[0]
        before = dict(original)
        record = notice_record(
            original,
            source_id="synthetic-source",
            camera_id="synthetic-camera",
            frame_index=serial,
            serial=serial,
            tracks=[track()],
        )
        assert original == before
        assert tuple(record[key] for key in fields) == tuple(original[key] for key in fields)
        assert record["decision_time_s"] == record["time_s"]
        assert record["track_ids"] == [1]
        assert record["boxes"] == [dict(time_s=at, track_id=1, box=BOX)]
        assert record["alert_id"] == f"synthetic-source:notice:{serial:09d}"


def test_evidence_metadata_preroll_postroll_and_track_boundaries() -> None:
    from campus_cctv.events.evidence import EvidenceBuffer
    from campus_cctv.events.schema import notice_record

    buffer = EvidenceBuffer(30)
    for at in (0, 0.1, 9.9, 10):
        assert buffer.observe(at, [track(), track(2)]) == []
    raw = WeaponRuntime(rule()).process(10, [track()], {1: 0.9})[0]
    raw = notice_record(
        raw,
        source_id="synthetic-source",
        camera_id="synthetic-camera",
        frame_index=100,
        serial=0,
        tracks=[track()],
    )
    immediate = buffer.start(raw)
    assert immediate["evidence_status"] == "pending_postroll"
    assert [item["time_s"] for item in immediate["boxes"]] == [0, 0.1, 9.9, 10]
    for at in (10.1, 14.9, 15 - 0.5e-9):
        ready = buffer.observe(at, [track(), track(2)])
    # The end-minus-epsilon condition is the frozen metadata selection boundary.
    ready += buffer.observe(15, [track(), track(2)])
    assert len(ready) == 1
    final = ready[0]
    assert [item["time_s"] for item in final["boxes"]] == [0, 0.1, 9.9, 10, 10.1, 14.9]
    assert all(item["track_id"] == 1 for item in final["boxes"])
    assert final["evidence_status"] == "complete_metadata"
    assert immediate["evidence_status"] == "pending_postroll"
    assert len(immediate["boxes"]) == 4
    for key in ("time_s", "decision_time_s", "kind", "score", "track_id", "parent"):
        assert final[key] == immediate[key] == raw[key]


def test_evidence_metadata_clips_to_source_and_preserves_parent() -> None:
    from campus_cctv.events.evidence import EvidenceBuffer
    from campus_cctv.events.schema import notice_record

    runtime = WeaponRuntime(rule())
    buffer = EvidenceBuffer(3)
    immediate = []
    for serial, at in enumerate((0, 1)):
        buffer.observe(at, [track()])
        notice = runtime.process(at, [track()], {1: 0.9})[0]
        notice = notice_record(
            notice,
            source_id="synthetic-source",
            camera_id="synthetic-camera",
            frame_index=serial,
            serial=serial,
            tracks=[track()],
        )
        immediate.append(buffer.start(notice))
    buffer.observe(2.9, [track()])
    final = buffer.finish()
    assert len(final) == 2
    assert final[0]["parent_alert_id"] == final[1]["parent_alert_id"]
    assert [item["kind"] for item in final] == ["NEW", "UPDATE"]
    assert all(record["evidence_end_s"] == 3 for record in final)
    assert [item["time_s"] for item in final[0]["boxes"]] == [0, 1, 2.9]
