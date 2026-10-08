"""Causal video decoding and source-time sampling."""

from __future__ import annotations

import math
from collections.abc import Iterator
from pathlib import Path

import numpy as np


def sampled_frames(path: str | Path, rate: float = 10) -> Iterator[tuple[int, float, np.ndarray]]:
    """Yield the first decoded frame at or after each source-time deadline.

    Decoder timestamps must increase. Missing or non-monotonic timing is an
    error; this reader does not invent a frame rate or silently drop late work.
    """
    if not Path(path).is_file():
        raise FileNotFoundError("Video is missing; datasets are not included with this repository.")
    if rate <= 0 or not math.isfinite(rate):
        raise ValueError("Analysis rate must be positive and finite")
    import cv2

    capture = cv2.VideoCapture(str(path))
    if not capture.isOpened():
        raise OSError("The video decoder could not open the supplied source")
    fps = capture.get(cv2.CAP_PROP_FPS)
    if not math.isfinite(fps) or fps <= 0:
        capture.release()
        raise ValueError("Missing video rate; a time base cannot be invented")
    expected_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    index, previous, next_due = 0, -1.0, 0.0
    try:
        while True:
            ok, image = capture.read()
            if not ok:
                break
            time_s = capture.get(cv2.CAP_PROP_POS_MSEC) / 1000
            if not math.isfinite(time_s) or time_s < 0 or time_s <= previous:
                raise ValueError("Decoder timestamps must be finite, non-negative and increasing")
            previous = time_s
            if time_s + 1e-9 >= next_due:
                yield index, time_s, image
                next_due = (math.floor(time_s * rate + 1e-8) + 1) / rate
            index += 1
        if expected_count and index != expected_count:
            raise OSError("Source decoding ended before its recorded frame count")
    finally:
        capture.release()


def video_duration(path: str | Path) -> float:
    """Read the same frame-count/rate duration used by the frozen file reader."""
    import cv2

    capture = cv2.VideoCapture(str(path))
    try:
        if not capture.isOpened():
            raise OSError("The video decoder could not open the supplied source")
        fps = capture.get(cv2.CAP_PROP_FPS)
        count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
        if not math.isfinite(fps) or fps <= 0 or count <= 0:
            raise ValueError("Source duration requires a valid rate and frame count")
        return count / fps
    finally:
        capture.release()
