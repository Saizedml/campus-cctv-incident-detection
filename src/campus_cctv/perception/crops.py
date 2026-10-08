"""Native person and hand crops, preserving the frozen crop geometry."""

from __future__ import annotations

from typing import Any

import numpy as np


def clip_box(box: list[float], width: int, height: int) -> list[int]:
    """Round outward, then clip an xyxy crop to its source frame."""
    x1, y1, x2, y2 = box
    return [
        max(0, int(np.floor(x1))),
        max(0, int(np.floor(y1))),
        min(width, int(np.ceil(x2))),
        min(height, int(np.ceil(y2))),
    ]


def crop_regions(
    track: dict[str, Any],
    frame_shape: tuple[int, ...],
    *,
    margin: float = 0.2,
    hand_scale: float = 0.45,
    minimum: int = 96,
    keypoint_confidence: float = 0.5,
) -> list[dict[str, Any]]:
    """Return a padded person crop and visible wrist-directed hand crops."""
    height, width = frame_shape[:2]
    x1, y1, x2, y2 = track["box"]
    w, h = x2 - x1, y2 - y1
    boxes = [
        (
            "person",
            clip_box(
                [x1 - margin * w, y1 - margin * h, x2 + margin * w, y2 + margin * h],
                width,
                height,
            ),
        )
    ]
    keypoints = np.asarray(track.get("keypoints", []))
    if keypoints.shape == (17, 3):
        for side, wrist, elbow in (("left_hand", 9, 7), ("right_hand", 10, 8)):
            if min(keypoints[wrist, 2], keypoints[elbow, 2]) < keypoint_confidence:
                continue
            centre = keypoints[wrist, :2] + 0.3 * (keypoints[wrist, :2] - keypoints[elbow, :2])
            radius = max(minimum, hand_scale * h) / 2
            boxes.append(
                (
                    side,
                    clip_box([*(centre - radius), *(centre + radius)], width, height),
                )
            )
    return [
        dict(kind=kind, box=box, track_id=track["track_id"])
        for kind, box in boxes
        if box[2] > box[0] and box[3] > box[1]
    ]
