"""Top-level CLI dispatcher.

Wires config + logging and routes to a flow. Thin on purpose; the real work
lives in flows/. Run with: ``python -m bestcase_agent.runner <command>``.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import List, Optional

from .config import AppConfig, Backend
from .logging_setup import get_logger

log = get_logger(__name__)


def _add_common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--backend", choices=[b.value for b in Backend])
    parser.add_argument("--executable", help="Path to BestCase.exe (optional).")


def _config_from_args(args: argparse.Namespace) -> AppConfig:
    config = AppConfig.from_env()
    updates = {}
    if getattr(args, "backend", None):
        updates["backend"] = Backend(args.backend)
    if getattr(args, "executable", None):
        updates["executable_path"] = Path(args.executable)
    return config.model_copy(update=updates) if updates else config


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(prog="bestcase-agent")
    sub = parser.add_subparsers(dest="command", required=True)

    p_inspect = sub.add_parser("inspect", help="Run the inspection flow.")
    _add_common(p_inspect)

    p_add = sub.add_parser("add-creditor", help="Enter one creditor from a job JSON.")
    _add_common(p_add)
    p_add.add_argument("job", help="Path to a creditor job JSON file.")
    p_add.add_argument("--index", type=int, default=0, help="Creditor index to enter.")

    args = parser.parse_args(argv)
    config = _config_from_args(args)

    if args.command == "inspect":
        from .flows.inspect_bestcase import run_inspection

        report = run_inspection(config)
        print(f"Inspection summary: {report}")
        return 0

    if args.command == "add-creditor":
        from .flows.add_single_creditor import add_single_creditor_from_json

        add_single_creditor_from_json(config, Path(args.job), index=args.index)
        return 0

    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
