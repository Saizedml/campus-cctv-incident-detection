"""Lazy YOLO pose and BoT-SORT adapter; importing this module loads no weights."""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import numpy as np

from campus_cctv.config import require_weights


class PoseTracker:
    """One source-local tracker with the frozen confidence and association settings."""

    def __init__(
        self,
        weights: str,
        *,
        imgsz: int = 1920,
        rate: float = 10,
        device: str = "cpu",
        quantize: int = 32,
        sha256: str | None = None,
    ) -> None:
        """Load explicit local weights; never download a default checkpoint."""
        path = require_weights(weights, sha256)
        from ultralytics import YOLO
        from ultralytics.trackers.bot_sort import BOTSORT

        self.model = YOLO(str(path))
        self.imgsz, self.device, self.rate = imgsz, device, rate
        self.quantize = quantize
        if quantize not in (16, 32):
            raise ValueError("Only FP16/FP32 inference is supported")
        args = SimpleNamespace(
            tracker_type="botsort",
            track_high_thresh=0.25,
            track_low_thresh=0.1,
            new_track_thresh=0.25,
            track_buffer=round(rate * 10),
            match_thresh=0.8,
            fuse_score=True,
            gmc_method="sparseOptFlow",
            proximity_thresh=0.5,
            appearance_thresh=0.8,
            with_reid=False,
            model="auto",
            device=device,
        )
        self.tracker = BOTSORT(args=args)
        self.last_time = -float("inf")

    def process(self, image: np.ndarray, time_s: float) -> list[dict[str, Any]]:
        """Predict pose then associate detections causally within this source."""
        if time_s <= self.last_time:
            raise ValueError("Tracker frames must be causal and consecutive")
        self.last_time = time_s
        result = self.model.predict(
            image,
            imgsz=self.imgsz,
            device=self.device,
            conf=0.1,
            iou=0.7,
            quantize=self.quantize,
            rect=True,
            verbose=False,
            save=False,
        )[0]
        tracked = self.tracker.update(result.boxes.cpu().numpy(), image)
        keypoints = result.keypoints.data.cpu().numpy()
        tracks = []
        for row in tracked:
            index = int(row[-1])
            if not 0 <= index < len(keypoints):
                raise ValueError("Tracker returned an invalid source detection index")
            tracks.append(
                dict(
                    box=row[:4].astype(float).tolist(),
                    track_id=int(row[4]),
                    score=float(row[5]),
                    keypoints=keypoints[index].astype(float).tolist(),
                )
            )
        return tracks
