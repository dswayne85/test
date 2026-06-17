#!/usr/bin/env python
"""Dump control identifiers for a specific window to output/reports/.

Run on the Best Case machine:
    python scripts/dump_controls.py --title-re ".*Creditor.*" [--backend uia|win32]
    python scripts/dump_controls.py            # dumps the current top window

Use this repeatedly as you open different Best Case dialogs to capture the real
selectors (auto_id / control_type / title) needed for app/selectors.py.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from bestcase_agent.adapters.bestcase_adapter import BestCaseAdapter  # noqa: E402
from bestcase_agent.config import AppConfig, Backend  # noqa: E402
from bestcase_agent.logging_setup import setup_logging  # noqa: E402
from bestcase_agent.state.session import Session  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Dump control identifiers.")
    parser.add_argument("--title-re", dest="title_re", default=None,
                        help="Regex for the window title to dump (default: top window).")
    parser.add_argument("--backend", choices=[b.value for b in Backend], default=None)
    parser.add_argument("--depth", type=int, default=None,
                        help="Limit control tree depth (default: full tree).")
    parser.add_argument("--label", default="controls", help="Filename label.")
    args = parser.parse_args(argv)

    config = AppConfig.from_env()
    if args.backend:
        config = config.model_copy(update={"backend": Backend(args.backend)})

    session = Session.create(config)
    setup_logging(config.logs_dir, level=config.log_level, run_id=session.run_id)

    adapter = BestCaseAdapter(config)
    adapter.connect_or_start()
    path = adapter.pwa.dump_controls(
        config.reports_dir,
        title_re=args.title_re,
        depth=args.depth,
        label=args.label,
    )
    print(f"Control dump written to: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
