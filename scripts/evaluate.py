"""Evaluate locally supplied notice/event JSON without running models."""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

from campus_cctv.evaluation import aggregate_metrics, evaluate


def main() -> None:
    """Write aggregate event metrics for a user-owned JSON evaluation input."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="JSON with events, alerts and exposures lists")
    parser.add_argument("--output", type=Path, required=True, help="Aggregate metrics JSON")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    if not args.input.is_file():
        parser.error("Evaluation input is missing. Supply your own saved notices and annotations.")
    data = json.loads(args.input.read_text(encoding="utf-8"))
    result = aggregate_metrics(evaluate(data["events"], data["alerts"], data["exposures"]))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    logging.info("Evaluation complete: %s", args.output)


if __name__ == "__main__":
    main()
