"""Render original, data-free diagrams and plots from permitted aggregate results."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

LOGGER = logging.getLogger(__name__)
ROOT = Path(__file__).resolve().parents[1]
BLUE = "#176B9C"
ORANGE = "#BC4C18"
GREEN = "#187666"
INK = "#193047"
PAPER = "#F7FAFC"


def style() -> None:
    """Use opaque light panels so charts remain legible in either GitHub theme."""
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 10,
            "text.color": INK,
            "axes.labelcolor": INK,
            "axes.edgecolor": "#B6C5CF",
            "axes.titleweight": "bold",
            "axes.facecolor": PAPER,
            "figure.facecolor": PAPER,
            "xtick.color": INK,
            "ytick.color": INK,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "svg.hashsalt": "campus-cctv-public-figures",
        }
    )


def save(fig: Figure, name: str) -> None:
    """Save reproducible PNG and SVG with no filesystem metadata."""
    destination = ROOT / "assets"
    destination.mkdir(exist_ok=True)
    fig.savefig(destination / f"{name}.png", dpi=150, bbox_inches="tight")
    fig.savefig(destination / f"{name}.svg", bbox_inches="tight", metadata={"Date": None})
    plt.close(fig)
    LOGGER.info("Generated %s", name)


def curve_plot(data: dict[str, Any]) -> None:
    """Compare frozen validation and locked-test aggregates at all six rules."""
    fig, axes = plt.subplots(2, 2, figsize=(12.8, 8.8))
    for row, task in enumerate(("weapons", "falls")):
        records = data[task]
        rates = np.array([x["meva_test_fa_h"] for x in records])
        recalls = np.array([x["recall"] * 100 for x in records])
        q = [x["q"] for x in records]
        validation = data["validation_recall"][task]
        by_q = {point["q"]: point for point in validation}
        if set(by_q) != set(q):
            raise ValueError(f"Expected validation recall at every frozen rule for {task}.")
        validation_rates = [record["validation_fa_h"] for record in records]
        validation_recalls = [100 * by_q[value]["hits"] / by_q[value]["total"] for value in q]
        ax = axes[row, 0]
        ax.plot(
            validation_rates,
            validation_recalls,
            "s--",
            color=GREEN,
            label="validation (tuning footage)",
        )
        ax.plot(rates, recalls, "o-", color=BLUE, label="locked test (unseen site)")
        for x, y, label in zip(rates, recalls, q, strict=True):
            ax.annotate(
                f"q{label:g}",
                (x, y),
                xytext=(4, 6),
                textcoords="offset points",
                fontsize=8,
            )
        for x, y, label in zip(validation_rates, validation_recalls, q, strict=True):
            ax.annotate(
                f"q{label:g}",
                (x, y),
                xytext=(4, -12),
                textcoords="offset points",
                fontsize=8,
                color=GREEN,
            )
        ax.set_title(f"{task.title()}: frozen operating points")
        ax.set_xscale("log")
        ax.set_ylim(0, 100)
        ax.set_xlabel("False alerts per camera-hour (log scale)")
        ax.set_ylabel("Event recall (%)")
        ax.grid(alpha=0.18)
        ax.legend(loc="lower right", fontsize=8)
        ax = axes[row, 1]
        x = np.arange(len(q))
        for field, label, colour, marker in (
            ("validation_fa_h", "validation (tuning footage)", GREEN, "s"),
            ("meva_test_fa_h", "locked test (unseen site)", BLUE, "o"),
            ("nwpu_fa_h", "independent NWPU test", ORANGE, "^"),
        ):
            ax.plot(x, [r[field] for r in records], marker=marker, color=colour, label=label)
        ax.set_xticks(x, [f"{v:g}" for v in q])
        ax.set_yscale("log")
        ax.set_xlabel("Rule q (validation false-alert budget per camera-hour)")
        ax.set_ylabel("New false alerts per camera-hour (log scale)")
        ax.set_title(f"{task.title()}: validation-to-test transfer")
        ax.grid(alpha=0.18)
        ax.legend(fontsize=8)
    fig.suptitle("Recall transfers unevenly; false-alert budgets do not transfer", fontsize=16)
    fig.text(
        0.05,
        0.01,
        "Unseen site refers to MEVA false-alert footage; recall uses the held-out weapon camera or independent falls collection.\n"
        "Validation is tuning footage. Falls rules are not nested thresholds; lines join operating points, not interpolated results.\n"
        "Original criteria: NOT MET. Weapons revised: MET (post-hoc). Falls revised: NOT MET (pre-test). Sources: docs/results.md.",
        fontsize=9,
    )
    fig.tight_layout(rect=(0, 0.09, 1, 0.96))
    save(fig, "recall_false_alerts")


def observation_plot(data: dict[str, Any]) -> None:
    """Plot assistant observations without implying adjudicated causal labels."""
    fig, axes = plt.subplots(1, 2, figsize=(12, 5.5))
    for ax, key, title, colour in (
        (axes[0], "weapons_review", "Weapons: random sample of 300 views", BLUE),
        (axes[1], "falls_review", "Falls: all 828 lower-budget alerts", ORANGE),
    ):
        group = data[key]
        categories = group["categories"]
        if key == "falls_review":
            categories = [x for x in categories if x["label"] in {"sitting", "riding", "walking"}]
        labels = [x["label"] for x in categories]
        values = [x["share_percent"] for x in categories]
        errors = np.array(
            [
                [x["share_percent"] - x["wilson95_percent"][0] for x in categories],
                [x["wilson95_percent"][1] - x["share_percent"] for x in categories],
            ]
        )
        bars = ax.barh(labels, values, xerr=errors, capsize=3, color=colour, alpha=0.92)
        for bar, item in zip(bars, categories, strict=True):
            ax.text(
                item["wilson95_percent"][1] + 1,
                bar.get_y() + bar.get_height() / 2,
                f"{item['count']}/{group['total']}",
                va="center",
                fontsize=9,
            )
        ax.invert_yaxis()
        ax.set_xlim(0, 70)
        ax.set_title(title)
        ax.set_xlabel("Share of reviewed items (%), with Wilson 95% interval")
        ax.grid(axis="x", alpha=0.18)
    fig.suptitle("Look-alikes and everyday postures generate alerts", fontsize=16)
    fig.text(
        0.05,
        0.015,
        "Weapons: 300 unique sampled views; selected categories only. Mops, notebook edges and pens are qualitative examples.\n"
        "Falls: 828 alerts; evidence can repeat across rules. Observation labels are separate from model guesses and human review.",
        fontsize=9,
    )
    fig.tight_layout(rect=(0, 0.10, 1, 0.94))
    save(fig, "false_alert_causes")


def latency_plot(data: dict[str, Any]) -> None:
    """Keep footage-time detection delay visibly separate from the failed real-time test."""
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 5.4))
    for ax, task in zip(axes, ("weapons", "falls"), strict=True):
        records = [r for r in data[task] if r["q"] in (2, 5)]
        x = np.arange(len(records))
        width = 0.33
        ax.bar(
            x - width / 2,
            [r["median_s"] for r in records],
            width,
            label="Median",
            color=GREEN,
        )
        ax.bar(x + width / 2, [r["p95_s"] for r in records], width, label="p95", color=BLUE)
        ax.set_xticks(x, ["Alert now (q2)", "Check when free (q5)"])
        ax.set_title(
            f"{task.title()} · "
            + ("footage time at nominal 2 fps" if task == "weapons" else "footage time")
        )
        ax.set_ylim(0, 5.5)
        ax.set_ylabel("Delay in seconds (detected incidents only)")
        ax.legend()
        ax.grid(axis="y", alpha=0.18)
        for xx, r in zip(x, records, strict=True):
            ax.text(
                xx - width / 2,
                r["median_s"] + 0.10,
                f"{r['median_s']:.1f}",
                ha="center",
                fontsize=9,
            )
            ax.text(
                xx + width / 2,
                r["p95_s"] + 0.10,
                f"{r['p95_s']:.1f}",
                ha="center",
                fontsize=9,
            )
    fig.suptitle("Detection delay in recorded footage is not live delivery time", fontsize=16)
    best_p95 = min(data["gi"], key=lambda record: max(record["falls_p95_s"]))["falls_p95_s"]
    fig.text(
        0.06,
        0.025,
        "Combined real-time test: not passed. In the best completed multi-feed run, "
        f"95th-percentile falls alert delay was about {max(best_p95):,.0f} s (limit 10 s).\n"
        "These bars exclude queueing, and missed incidents do not enter the median or p95 values.",
        color=ORANGE,
        fontsize=10,
        weight="bold",
    )
    fig.tight_layout(rect=(0, 0.13, 1, 0.95))
    save(fig, "alert_latency")


def box(
    ax: Axes,
    x: float,
    y: float,
    width: float,
    height: float,
    title: str,
    colour: str = BLUE,
) -> None:
    """Draw one original architecture node."""
    patch = FancyBboxPatch(
        (x, y),
        width,
        height,
        boxstyle="round,pad=0.015,rounding_size=0.025",
        edgecolor=colour,
        facecolor="white",
        linewidth=1.8,
    )
    ax.add_patch(patch)
    ax.text(
        x + width / 2,
        y + height / 2,
        title,
        ha="center",
        va="center",
        fontsize=11,
        color=INK,
    )


def arrow(ax: Axes, start: tuple[float, float], end: tuple[float, float]) -> None:
    """Draw a directed flow connection."""
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle="-|>",
            color="#70889A",
            mutation_scale=13,
            linewidth=1.5,
        )
    )


def architecture() -> None:
    """Create the original repository-native architecture motif."""
    fig, ax = plt.subplots(figsize=(12, 5.6))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    box(ax, 0.025, 0.4, 0.15, 0.17, "Video\nframes")
    box(ax, 0.225, 0.4, 0.17, 0.17, "Shared pose\nand tracks")
    box(ax, 0.465, 0.64, 0.23, 0.18, "Weapon detector\n+ vision-language check")
    box(ax, 0.465, 0.17, 0.23, 0.18, "Pose geometry\n+ person-down head", GREEN)
    box(ax, 0.765, 0.4, 0.20, 0.17, "Alert grouping\nnew / update", ORANGE)
    for a, b in (
        ((0.175, 0.485), (0.22, 0.485)),
        ((0.395, 0.50), (0.455, 0.71)),
        ((0.395, 0.46), (0.455, 0.27)),
        ((0.70, 0.71), (0.755, 0.52)),
        ((0.70, 0.27), (0.755, 0.45)),
    ):
        arrow(ax, a, b)
    ax.text(0.86, 0.30, "Evidence → human review", ha="center", fontsize=10)
    ax.text(
        0.03,
        0.95,
        "One shared front end. Task-specific decisions.",
        fontsize=18,
        weight="bold",
    )
    ax.text(
        0.03,
        0.01,
        "Research prototype · Scores are model confidence, not probabilities.",
        fontsize=9,
    )
    save(fig, "architecture")


def social_preview() -> None:
    """Generate a fixed-size, frame-free social preview below the media limit."""
    fig = plt.figure(figsize=(12.8, 6.4), dpi=100, facecolor="#10263D")
    ax = fig.add_axes((0, 0, 1, 1), facecolor="#10263D")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.text(0.065, 0.84, "CAMPUS CCTV", fontsize=34, weight="bold", color="white")
    ax.text(0.065, 0.72, "INCIDENT DETECTION", fontsize=34, weight="bold", color="white")
    ax.text(
        0.065,
        0.61,
        "A research prototype for evidence-led human review.",
        fontsize=18,
        color="#BCD7E7",
    )
    for x, label, colour in (
        (0.07, "SHARED\nPERCEPTION", BLUE),
        (0.38, "WEAPONS\n+ PERSON DOWN", GREEN),
        (0.69, "EVIDENCE\n+ HUMAN REVIEW", ORANGE),
    ):
        ax.add_patch(
            FancyBboxPatch(
                (x, 0.28),
                0.24,
                0.19,
                boxstyle="round,pad=0.012",
                facecolor=colour,
                edgecolor="none",
            )
        )
        ax.text(
            x + 0.12,
            0.375,
            label,
            ha="center",
            va="center",
            fontsize=16,
            weight="bold",
            color="white",
        )
    for x in (0.315, 0.625):
        ax.add_patch(
            FancyArrowPatch(
                (x, 0.375),
                (x + 0.055, 0.375),
                arrowstyle="-|>",
                color="white",
                mutation_scale=20,
                linewidth=2,
            )
        )
    ax.text(
        0.065,
        0.15,
        "Transparent evaluation. Frozen rules. Documented failures.",
        fontsize=16,
        color="#BCD7E7",
    )
    ax.text(
        0.065,
        0.065,
        "Max Blunden-Slusarski · Research internship prototype",
        fontsize=13,
        color="white",
    )
    target = ROOT / "assets" / "social_preview.png"
    fig.savefig(target, dpi=100, facecolor=fig.get_facecolor())
    plt.close(fig)
    LOGGER.info("Generated social_preview")


def main() -> None:
    """Build the complete original figure set from the committed aggregates."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    style()
    data = json.loads((ROOT / "results" / "aggregate.json").read_text())
    curve_plot(data)
    observation_plot(data)
    latency_plot(data)
    architecture()
    social_preview()


if __name__ == "__main__":
    main()
