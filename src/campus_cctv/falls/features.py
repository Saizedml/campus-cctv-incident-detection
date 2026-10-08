"""Exact incremental features used by the frozen geometry-only temporal head."""

from __future__ import annotations

import collections
import heapq
import math
from typing import Any

import numpy as np

FB0_COLUMNS = [68, 69, 70, 72, 73, 74]


class GeometryFeatures:
    """Incremental form of frozen features(); exact parity checked before launch."""

    def __init__(self) -> None:
        """Initialise empty source-local track state."""
        self.state = {}
        self.windows = {}

    def step(self, row: dict[str, Any]) -> list[tuple[int, np.ndarray, np.ndarray, np.ndarray]]:
        """Compute causal features and zero-padded 20-step FB0 inputs."""
        output = []
        t = row["time_s"]
        for tr in row["tracks"]:
            tid = tr["track_id"]
            box = np.asarray(tr["box"], np.float32)
            kp = np.asarray(tr["keypoints"], np.float32)
            valid = (kp[:, 2] >= 0.25) & np.isfinite(kp).all(axis=1)
            h = max(float(box[3] - box[1]), 1.0)
            w = max(float(box[2] - box[0]), 1.0)
            centre = (box[:2] + box[2:]) / 2
            hip_ok = bool(valid[11] and valid[12])
            shoulder_ok = bool(valid[5] and valid[6])
            hip = (kp[11, :2] + kp[12, :2]) / 2 if hip_ok else centre
            shoulder = (kp[5, :2] + kp[6, :2]) / 2 if shoulder_ok else hip
            torso = float(np.linalg.norm(shoulder - hip)) if hip_ok and shoulder_ok else 0.0
            scale = torso if torso >= 0.1 * h else h
            xy = np.clip((kp[:, :2] - hip) / scale, -5, 5)
            xy[~valid] = 0
            conf = np.clip(kp[:, 2], 0, 1)
            conf[~valid] = 0
            st = self.state.setdefault(tid, dict(low=[], high=[], last=None, cy=None))
            if w / h <= 0.75:
                heapq.heappush(st["low"], -h)
                heapq.heappush(st["high"], -heapq.heappop(st["low"]))
                if len(st["high"]) > len(st["low"]):
                    heapq.heappush(st["low"], -heapq.heappop(st["high"]))
            standing = (
                (
                    -st["low"][0]
                    if len(st["low"]) > len(st["high"])
                    else (-st["low"][0] + st["high"][0]) / 2
                )
                if st["low"]
                else h
            )
            dt = t - st["last"] if st["last"] is not None else 0
            velocity_ok = 0 < dt <= 0.25
            velocity = (float(centre[1]) - st["cy"]) / (dt * standing) if velocity_ok else 0.0
            angle_ok = hip_ok and shoulder_ok and (torso >= 0.1 * h)
            angle = (
                math.atan2(abs(float(hip[0] - shoulder[0])), abs(float(hip[1] - shoulder[1])))
                / (math.pi / 2)
                if angle_ok
                else 0.0
            )
            geometry = [
                min(w / h, 5),
                min(h / standing, 3),
                np.clip(velocity, -5, 5),
                angle,
            ]
            x = np.r_[
                np.c_[xy, conf].ravel(),
                valid.astype(np.float32),
                geometry,
                [1, 1, velocity_ok, angle_ok],
            ].astype(np.float32)
            assert x.shape == (76,) and np.isfinite(x).all()
            window = self.windows.setdefault(tid, collections.deque(maxlen=20))
            if not velocity_ok:
                window.clear()
            window.append(x)
            padded = np.zeros((20, 6), np.float32)
            padded[-len(window) :] = np.asarray(window)[:, FB0_COLUMNS]
            output.append((tid, box, x, padded))
            st.update(last=t, cy=float(centre[1]))
        return output
