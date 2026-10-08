"""Single-source combined inference with the frozen task decision rules.

This serial adapter makes the curated components executable. It does not claim
that a combined feed count meets the latency budget: the combined real-time test failed.
"""

from __future__ import annotations

import json
import logging
import math
from collections import deque
from pathlib import Path
from typing import Any

from campus_cctv.config import load_config, operating_point, require_weights
from campus_cctv.events.evidence import EvidenceBuffer
from campus_cctv.events.schema import notice_record
from campus_cctv.falls.rules import FallsRule, FallsRuntime
from campus_cctv.weapons.rules import WeaponRule, WeaponRuntime

LOGGER = logging.getLogger(__name__)


def check_inputs(config: dict[str, Any]) -> None:
    """Check local inputs without importing inference libraries or using a device."""
    for model in ("pose", "weapon", "falls"):
        require_weights(config[f"{model}_weights"], config.get(f"{model}_sha256"))
    if not (Path(config["verifier_weights"]) / "config.json").is_file():
        raise FileNotFoundError("Supply the frozen local verifier snapshot; see docs/data.md.")
    if not Path(config["source_video"]).is_file():
        raise FileNotFoundError("Supply an authorised local video; datasets are not included.")
    for key in ("weapons_config", "falls_config"):
        load_config(config[key])


def run_pipeline(config: dict[str, Any]) -> int:
    """Write immediate decisions and separately completed evidence-metadata JSONL.

    Weights and input data are explicit local files. The output is a notice
    stream: NEW and UPDATE are separate records. A separate completed metadata
    stream adds source-clipped post-roll boxes for event evaluation. This runner
    writes no evidence movies; later context never delays the immediate decision.
    """
    check_inputs(config)
    output = Path(config["output"])
    output.parent.mkdir(parents=True, exist_ok=True)
    evidence_output = Path(
        config.get("evidence_output", output.with_name(output.stem + ".evidence.jsonl"))
    )
    evidence_output.parent.mkdir(parents=True, exist_ok=True)
    if output == evidence_output:
        raise ValueError("Immediate and completed evidence outputs must be distinct")
    if output.exists() or evidence_output.exists():
        raise FileExistsError("Output already exists; choose a fresh output file.")
    import cv2
    import torch
    from PIL import Image

    from campus_cctv.falls.head import FallsHead
    from campus_cctv.perception.pose import PoseTracker
    from campus_cctv.perception.video import sampled_frames, video_duration
    from campus_cctv.weapons.detector import CropDetector, normalise_detections
    from campus_cctv.weapons.verifier import Verifier, select_evidence

    torch.manual_seed(0)
    torch.set_num_threads(4)
    cv2.setNumThreads(1)
    weapon_config = load_config(config["weapons_config"])
    falls_config = load_config(config["falls_config"])
    points = [operating_point(value) for value in config["operating_points"]]
    weapons = {
        q: WeaponRuntime(WeaponRule(**weapon_config["operating_points"][q]), q) for q in points
    }
    falls = {q: FallsRuntime(FallsRule(**falls_config["operating_points"][q]), q) for q in points}
    pose = PoseTracker(
        config["pose_weights"],
        imgsz=config["pose_image_size"],
        rate=config["perception_hz"],
        device=config["device"],
        sha256=config.get("pose_sha256"),
    )
    detector = CropDetector(
        config["weapon_weights"],
        device=config["device"],
        sha256=config.get("weapon_sha256"),
    )
    head = FallsHead(config["falls_weights"], config.get("falls_sha256"))
    verifier = Verifier(config["verifier_weights"], config["device"])
    history: deque[dict[str, Any]] = deque()
    images: deque[tuple[float, int, Any]] = deque()
    next_check, count = 0.0, 0
    evidence = EvidenceBuffer(video_duration(config["source_video"]))
    with (
        output.open("x", encoding="utf-8") as stream,
        evidence_output.open("x", encoding="utf-8") as completed,
    ):
        for index, now, image in sampled_frames(config["source_video"], config["perception_hz"]):
            tracks = pose.process(image, now)
            for record in evidence.observe(now, tracks):
                completed.write(json.dumps(record, allow_nan=False) + "\n")
            completed.flush()
            check = now + 1e-9 >= next_check
            detections = normalise_detections(detector.predict(image, tracks)) if check else []
            row = dict(time_s=now, frame_index=index, tracks=tracks, detections=detections)
            history.append(row)
            if check:
                next_check = (math.floor(now * 2 + 1e-8) + 1) / 2
                images.append((now, index, image.copy()))
            while images and images[0][0] < now - 10 - 1e-9:
                images.popleft()
            while len(history) > 1 and history[1]["time_s"] < now - 10 - 1e-9:
                history.popleft()
            frame_map = {frame_index: frame for _, frame_index, frame in images}
            answers: dict[int, str] = {}

            def classify(track_id: int, at: float) -> str:
                if track_id in answers:
                    return answers[track_id]
                views = []
                for crop in select_evidence(list(history), at, track_id):
                    frame = frame_map[crop["frame_index"]]
                    x1, y1, x2, y2 = map(int, crop["crop_box"])
                    region = frame[
                        max(0, y1) : min(frame.shape[0], y2),
                        max(0, x1) : min(frame.shape[1], x2),
                    ]
                    if not region.size:
                        raise ValueError("Empty generating crop in verifier evidence")
                    views.append(Image.fromarray(cv2.cvtColor(region, cv2.COLOR_BGR2RGB)))
                context = image.copy()
                track = next(item for item in tracks if item["track_id"] == track_id)
                x1, y1, x2, y2 = map(int, track["box"])
                cv2.rectangle(context, (x1, y1), (x2, y2), (0, 255, 255), 2)
                views.append(Image.fromarray(cv2.cvtColor(context, cv2.COLOR_BGR2RGB)))
                answers[track_id] = verifier.predict(views)
                return answers[track_id]

            best: dict[int, float] = {}
            for detection in detections:
                if detection["name"] in {"knife", "firearm"}:
                    tid = detection["track_id"]
                    best[tid] = max(best.get(tid, -1.0), float(detection["score"]))
            notices = []
            for runtime in weapons.values():
                notices.extend(runtime.process(now, tracks, best, check=check, verdict=classify))
            for track_id, box, scores in head.process(row):
                for runtime in falls.values():
                    notice = runtime.process(
                        now,
                        track_id,
                        float(scores[0]),
                        float(scores[1]),
                        box=box,
                        height=image.shape[0],
                    )
                    if notice is not None:
                        notices.append(notice)
            for notice in notices:
                notice = notice_record(
                    notice,
                    source_id=config["source_id"],
                    camera_id=config["camera_id"],
                    frame_index=index,
                    serial=count,
                    tracks=tracks,
                )
                notice = evidence.start(notice)
                stream.write(json.dumps(notice, allow_nan=False) + "\n")
                stream.flush()
                count += 1
        for record in evidence.finish():
            completed.write(json.dumps(record, allow_nan=False) + "\n")
    LOGGER.info("Wrote %d immediate notices and completed evidence metadata records", count)
    return count
