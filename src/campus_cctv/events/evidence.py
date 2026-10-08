"""Complete source-time evidence metadata without delaying notice delivery."""

from __future__ import annotations

from collections import deque
from copy import deepcopy
from typing import Any


class EvidenceBuffer:
    """Collect same-track boxes over [decision−10s, decision+5s).

    This is metadata only: no crops, images or movies are written. Immediate
    notices remain provisional until their available post-roll is complete.
    """

    def __init__(self, duration_s: float) -> None:
        """Create source-local metadata state with an explicit source duration."""
        if duration_s <= 0:
            raise ValueError("Source duration must be positive")
        self.duration_s = duration_s
        self.history: deque[dict[str, Any]] = deque()
        self.pending: list[dict[str, Any]] = []
        self.last_time = -float("inf")
        self.parents: dict[tuple, str] = {}
        self.groups: dict[str, set[int]] = {}

    def observe(self, time_s: float, tracks: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Append observed boxes and return metadata records whose post-roll ended."""
        if time_s <= self.last_time:
            raise ValueError("Evidence observations must be strictly increasing")
        self.last_time = time_s
        self.history.append(dict(time_s=time_s, tracks=deepcopy(tracks)))
        while self.history and self.history[0]["time_s"] < time_s - 10:
            self.history.popleft()
        for record in self.pending:
            if record["decision_time_s"] < time_s < record["evidence_end_s"] - 1e-9:
                record["boxes"].extend(
                    dict(time_s=time_s, track_id=track["track_id"], box=list(track["box"]))
                    for track in tracks
                    if track["track_id"] in record["track_ids"]
                )
        ready = [record for record in self.pending if record["evidence_end_s"] <= time_s + 1e-9]
        self.pending = [
            record for record in self.pending if record["evidence_end_s"] > time_s + 1e-9
        ]
        for record in ready:
            record["evidence_status"] = "complete_metadata"
        return ready

    def start(self, notice: dict[str, Any]) -> dict[str, Any]:
        """Register an unchanged decision and return its immediate provisional form."""
        record = deepcopy(notice)
        now, tid = record["decision_time_s"], record["track_id"]
        if now != self.last_time:
            raise ValueError("Register a notice after observing its decision frame")
        key = (record["task"], record["q"], record.get("parent", tid))
        if record["kind"] == "NEW":
            self.parents[key] = record["alert_id"]
        if key not in self.parents:
            raise ValueError("UPDATE has no earlier source-local NEW notice")
        parent = self.parents[key]
        members = self.groups.setdefault(parent, set())
        members.add(tid)
        record.update(
            parent_alert_id=parent,
            open_alert_track_ids=sorted(members),
            evidence_start_s=max(0, now - 10),
            evidence_end_s=min(self.duration_s, now + 5),
            evidence_status="pending_postroll",
            score_label="uncalibrated score",
            label="WEAPON" if record["task"] == "weapons" else "person down",
        )
        record["boxes"] = [
            dict(time_s=row["time_s"], track_id=tid, box=list(track["box"]))
            for row in self.history
            if record["evidence_start_s"] <= row["time_s"] < record["evidence_end_s"] - 1e-9
            for track in row["tracks"]
            if track["track_id"] == tid
        ]
        self.pending.append(deepcopy(record))
        return record

    def finish(self) -> list[dict[str, Any]]:
        """Finalise metadata at a successfully decoded end of source."""
        result, self.pending = self.pending, []
        for record in result:
            record["evidence_status"] = "complete_metadata"
        return result
