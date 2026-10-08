"""Open a standalone local dashboard; no model or web server is started."""

from __future__ import annotations

import argparse
import logging
import tempfile
import webbrowser
from pathlib import Path

from . import write_dashboard


def main() -> None:
    """Generate the offline interface and optionally open the default browser."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Directory for generated standalone HTML")
    parser.add_argument("--no-open", action="store_true", help="Generate without opening a browser")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    directory = args.output or Path(tempfile.mkdtemp(prefix="campus-dashboard-"))
    page = write_dashboard(directory)
    logging.info("Offline dashboard: %s", page)
    if not args.no_open:
        webbrowser.open(page.resolve().as_uri())


if __name__ == "__main__":
    main()
