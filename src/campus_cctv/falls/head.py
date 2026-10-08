"""Lazy FB0 loading and causal geometry-head execution."""

from __future__ import annotations

from typing import Any

import numpy as np

from campus_cctv.config import require_weights
from campus_cctv.falls.features import GeometryFeatures


class FallsHead:
    """Six-class geometry-only TCN with the frozen twenty-step input window."""

    def __init__(self, weights: str, sha256: str | None = None) -> None:
        """Load a trusted local final checkpoint on CPU without downloading files."""
        path = require_weights(weights, sha256)
        import torch

        from campus_cctv.falls.model import TCN

        self.model = TCN(inputs=6, channels=64, dilations=(1, 2, 4), dropout=0.1)
        checkpoint = torch.load(path, map_location="cpu", weights_only=False)
        self.model.load_state_dict(checkpoint["state_dict"], strict=True)
        self.model.eval()
        self.features = GeometryFeatures()

    def process(self, row: dict[str, Any]) -> list[tuple[int, list[float], np.ndarray]]:
        """Return track ID, box and six uncalibrated class outputs."""
        import torch

        result = []
        for track_id, box, _features, window in self.features.step(row):
            with torch.inference_mode():
                scores = torch.softmax(self.model(torch.from_numpy(window[None])), dim=-1)[
                    0
                ].numpy()
            result.append((track_id, box.tolist(), scores))
        return result
