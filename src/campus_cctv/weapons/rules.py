"""Causal translation of the frozen weapon replay kernel.

Veto is evaluated before cooldown mutation. Source time, rather than wall time,
controls evidence windows and continuation. Each runtime belongs to one source
and one operating point; changing a source requires a new runtime.
"""

from __future__ import annotations

from collections import deque
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from typing import Any

from campus_cctv.events import box_iou


@dataclass(frozen=True)
class WeaponRule:
    """Frozen temporal rule; q is a validation budget, not a test rate."""

    tau_a: float
    tau_hi: float
    veto_hi: float
    statistic: str = "best"
    k: int = 1
    window: float = 2.0
    tau_v: float = 0.0

    def __post_init__(self) -> None:
        if self.statistic not in {"best", "mean_top3"} or self.k < 1:
            raise ValueError("Invalid frozen score statistic or persistence count")
        if self.window == 0:
            raise ValueError("Use a positive time window or -1 for track lifetime")


@dataclass
class _Track:
    box: Sequence[float] = (0, 0, 0, 0)
    seen: float = -1e30
    raw: deque = field(default_factory=deque)
    low: deque = field(default_factory=deque)


@dataclass
class _Open:
    start: float
    identifier: int
    members: list[int]


def _stat(values: deque, mean: bool) -> float:
    scores = sorted((item[1] for item in values), reverse=True)
    if not scores:
        return -1.0
    return sum(scores[:3]) / min(len(scores), 3) if mean else scores[0]


class WeaponRuntime:
    """Emit deterministic NEW/UPDATE notices, requesting V only when required."""

    def __init__(self, rule: WeaponRule, q: str = "2.0") -> None:
        self.rule = rule
        self.q = q
        self.tracks: dict[int, _Track] = {}
        self.opens: list[_Open] = []
        self.last_time = -float("inf")

    def process(
        self,
        time_s: float,
        tracks: list[dict[str, Any]],
        scores: dict[int, float],
        *,
        check: bool = True,
        verdict: Callable[[int, float], str] | None = None,
    ) -> list[dict[str, Any]]:
        """Process one frame; verdict receives (track ID, source time).

        Missing V evidence raises rather than provisionally passing a candidate.
        A score above tau_hi bypasses V exactly as in the frozen rules.
        """
        if time_s <= self.last_time:
            raise ValueError("Source frames must have strictly increasing times")
        self.last_time = time_s
        for track in tracks:
            state = self.tracks.setdefault(int(track["track_id"]), _Track())
            state.box, state.seen = track["box"], time_s
        if not check:
            return []
        result = []
        rule = self.rule
        for track in sorted(tracks, key=lambda item: int(item["track_id"])):
            tid = int(track["track_id"])
            state = self.tracks[tid]
            score = scores.get(tid, -1.0)
            for values in (state.raw, state.low):
                while rule.window > 0 and values and values[0][0] <= time_s - rule.window + 1e-9:
                    values.popleft()
            if score >= 0:
                state.raw.append((time_s, score))
            if score >= rule.tau_v:
                state.low.append((time_s, score))
            high = _stat(state.raw, rule.statistic == "mean_top3")
            low = _stat(state.low, rule.statistic == "mean_top3")
            high_pass = score >= 0 and high >= rule.tau_hi
            if not high_pass and not (len(state.low) >= rule.k and low >= rule.tau_a):
                continue
            if high < rule.veto_hi:
                if verdict is None:
                    raise ValueError("Frozen rule requires a verifier answer for this candidate")
                answer = verdict(tid, time_s)
                if answer not in {"weapon", "not_weapon", "uncertain"}:
                    raise ValueError("Invalid verifier label")
                if answer == "not_weapon":
                    continue
            opened = next(
                (
                    item
                    for item in self.opens
                    if time_s - item.start < 60 - 1e-9 and tid in item.members
                ),
                None,
            )
            if opened is None:
                opened = next(
                    (
                        item
                        for item in self.opens
                        if time_s - item.start < 60 - 1e-9
                        and any(
                            time_s - self.tracks[member].seen <= 2 + 1e-9
                            and box_iou(state.box, self.tracks[member].box) >= 0.3 - 1e-12
                            for member in item.members
                        )
                    ),
                    None,
                )
            fresh = opened is None
            if fresh:
                opened = _Open(time_s, len(self.opens), [tid])
                self.opens.append(opened)
            elif tid not in opened.members:
                opened.members.append(tid)
            result.append(
                dict(
                    q=self.q,
                    task="weapons",
                    time_s=time_s,
                    track_id=tid,
                    kind="NEW" if fresh else "UPDATE",
                    parent=opened.identifier,
                    score=high if high_pass else low,
                    high_pass=high_pass,
                    lower_count=len(state.low),
                    lower_score=low,
                )
            )
            if fresh and rule.window < 0:
                state.raw.clear()
                state.low.clear()
        return result
