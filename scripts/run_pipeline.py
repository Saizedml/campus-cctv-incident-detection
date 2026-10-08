"""Run explicit local models, or check supplied inputs without inference."""

from __future__ import annotations

import argparse
import logging

from campus_cctv.config import load_config
from campus_cctv.perception.pipeline import check_inputs, run_pipeline


def main() -> None:
    """Read the runtime YAML and execute the requested local-only operation."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default="configs/runtime.yaml")
    parser.add_argument("--check-inputs", action="store_true")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    try:
        config = load_config(args.config)
        if args.check_inputs:
            check_inputs(config)
            logging.info("Local input checks passed; no inference was run")
        else:
            run_pipeline(config)
    except (ValueError, OSError, ImportError) as error:
        logging.error("%s", error)
        raise SystemExit(2) from error


if __name__ == "__main__":
    main()
