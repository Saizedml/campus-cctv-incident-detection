"""R4 down-persistence OR fall-peak, followed by border veto and cooldown."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class FallsRule:
    """Parameters of one frozen falls operating point."""

    tau_down: float = 0.35
    T_p: float = 0.5
    tau_f: float = 0.95
    n: int = 1
    B: str = "off"
    enabled: bool = True
    arm: str = "fb0"
    family: str = "R4"
    fallback: bool = False

    def __post_init__(self) -> None:
        if self.family != "R4" or self.arm != "fb0" or self.B not in {"on", "off"}:
            raise ValueError("Only the frozen FB0 R4 rules are supported")
        if self.T_p < 0 or self.n < 1:
            raise ValueError("Invalid persistence settings")


@dataclass
class _State:
    last: float = -1e12
    down: float = -1e12
    n: int = 0
    opened: float = -1e12
    border: float = -1e12


class FallsRuntime:
    """Track-local R4 state; no identity merging or future context."""

    def __init__(self, rule: FallsRule, q: str = "2.0") -> None:
        self.rule, self.q = rule, q
        self.state: dict[int, _State] = {}

    def process(
        self,
        time_s: float,
        track_id: int,
        fall_score: float,
        down_score: float,
        *,
        box: list[float],
        height: int,
    ) -> dict[str, Any] | None:
        """Consume one observation; all eligible continuations remain UPDATEs."""
        rule = self.rule
        state = self.state.setdefault(track_id, _State())
        if time_s <= state.last:
            raise ValueError("Track observations must have strictly increasing times")
        if time_s - state.last > 0.250000001:
            state.down, state.n = -1e12, 0
        if down_score >= rule.tau_down:
            if state.down < 0:
                state.down = time_s
        else:
            state.down = -1e12
        state.n = (
            (state.n + 1 if time_s - state.last <= 0.150000001 else 1)
            if fall_score >= rule.tau_f
            else 0
        )
        reason = (1 if state.down >= 0 and time_s - state.down >= rule.T_p - 1e-9 else 0) | (
            4 if state.n >= rule.n else 0
        )
        margin = max(4, 0.01 * height)
        if box[1] <= margin or box[3] >= height - margin:
            state.border = time_s
        state.last = time_s
        if not rule.enabled or not reason or (rule.B == "on" and time_s - state.border <= 1 + 1e-9):
            return None
        fresh = time_s - state.opened >= 120 - 1e-9
        if fresh:
            state.opened = time_s
        return dict(
            q=self.q,
            task="falls",
            time_s=time_s,
            track_id=track_id,
            kind="NEW" if fresh else "UPDATE",
            box=box,
            reason=reason,
            score=max(fall_score, down_score),
            fall_score=fall_score,
            down_score=down_score,
        )
