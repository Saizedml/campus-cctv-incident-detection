"""RF-DETR-L crop inference and frozen class-aware full-frame NMS."""

from __future__ import annotations

from typing import Any

import numpy as np

from campus_cctv.config import require_weights
from campus_cctv.perception.crops import crop_regions

CLASSES = [
    "firearm",
    "phone",
    "knife",
    "wallet_purse",
    "banknote",
    "card",
    "keys",
    "remote_control",
    "scissors",
    "pen",
    "screwdriver",
    "flashlight",
]


def merge_detections(
    detections: list[dict[str, Any]], threshold: float = 0.5
) -> list[dict[str, Any]]:
    """NMS by detector class; retain the winning crop and track provenance."""
    import torch
    from torchvision.ops import nms

    kept = []
    for class_id in sorted({row["class_id"] for row in detections}):
        rows = [row for row in detections if row["class_id"] == class_id]
        boxes = torch.tensor([row["box"] for row in rows], dtype=torch.float32)
        scores = torch.tensor([row["score"] for row in rows], dtype=torch.float32)
        kept.extend(rows[index] for index in nms(boxes, scores, threshold).tolist())
    return sorted(kept, key=lambda row: -row["score"])


class CropDetector:
    """Frozen RF-DETR checkpoint with explicit local weights and class layout."""

    def __init__(self, weights: str, *, device: str = "cpu", sha256: str | None = None) -> None:
        """Load the checkpoint; no fallback model is silently substituted."""
        path = require_weights(weights, sha256)
        from rfdetr import RFDETR

        self.model = RFDETR.from_checkpoint(
            str(path), resolution=640, device="cpu" if device == "cpu" else "cuda"
        )
        if list(self.model.class_names) != CLASSES:
            raise ValueError("RF-DETR class layout differs from the frozen model")

    def predict(self, image: np.ndarray, tracks: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Evaluate native crops in frozen batches of two and merge detections."""
        regions = [region for track in tracks for region in crop_regions(track, image.shape)]
        detections = []
        for start in range(0, len(regions), 2):
            group = regions[start : start + 2]
            crops = [image[r["box"][1] : r["box"][3], r["box"][0] : r["box"][2]] for r in group]
            outputs = self.model.predict(
                [np.ascontiguousarray(crop[:, :, ::-1]) for crop in crops],
                threshold=0.001,
            )
            for region, result in zip(group, outputs, strict=True):
                raw = np.column_stack([result.xyxy, result.confidence, result.class_id])
                x1, y1, x2, y2 = region["box"]
                for box in raw:
                    class_id = int(box[5])
                    if not 0 <= class_id < len(CLASSES):
                        continue
                    mapped = [
                        max(x1, min(x2, float(box[0]) + x1)),
                        max(y1, min(y2, float(box[1]) + y1)),
                        max(x1, min(x2, float(box[2]) + x1)),
                        max(y1, min(y2, float(box[3]) + y1)),
                    ]
                    if mapped[2] <= mapped[0] or mapped[3] <= mapped[1]:
                        continue
                    detections.append(
                        dict(
                            box=mapped,
                            score=float(box[4]),
                            class_id=class_id,
                            name=CLASSES[class_id],
                            track_id=region["track_id"],
                            crop_kind=region["kind"],
                            crop_box=region["box"],
                        )
                    )
        return merge_detections(detections)


def normalise_detections(detections: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Keep finite weapon classes, retaining each generating crop's track ID."""
    result = []
    for item in detections:
        detection = dict(item)
        name = detection["name"]
        if name in {"pistol", "gun", "rifle", "Handgun", "Short_rifle"}:
            name = "firearm"
        if name not in {"knife", "firearm"}:
            continue
        detection["name"] = name
        if not np.isfinite(detection["score"]) or not np.isfinite(detection["box"]).all():
            raise ValueError("Non-finite detection")
        result.append(detection)
    return result
