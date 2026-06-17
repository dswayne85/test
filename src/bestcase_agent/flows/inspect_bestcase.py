"""Milestone 1 inspection flow.

Connects to Best Case, prints window info, dumps control identifiers, saves a
screenshot, and writes a summary report to output/reports/. This is the FIRST
thing to run on the Best Case machine.
"""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from ..adapters.bestcase_adapter import BestCaseAdapter
from ..config import AppConfig, Backend
from ..logging_setup import get_logger, setup_logging
from ..state.session import Session

log = get_logger(__name__)


def run_inspection(config: AppConfig) -> Path:
    """Run the full inspection and return the path to the summary report."""
    session = Session.create(config)
    setup_logging(config.logs_dir, level=config.log_level, run_id=session.run_id)
    log.info("=== Best Case inspection run %s (backend=%s) ===",
             session.run_id, config.backend.value)

    adapter = BestCaseAdapter(config)
    summary_lines: List[str] = [
        "# Best Case inspection report",
        f"run_id: {session.run_id}",
        f"timestamp: {datetime.now().isoformat(timespec='seconds')}",
        f"backend: {config.backend.value}",
        f"process_name: {config.process_name}",
        f"main_window_title_re: {config.main_window_title_re}",
        "",
    ]

    try:
        adapter.connect_or_start()
    except Exception as exc:  # noqa: BLE001
        summary_lines.append(f"CONNECT FAILED: {exc!r}")
        report = _write_summary(config.reports_dir, session.run_id, summary_lines)
        log.error("Inspection could not connect to Best Case: %r", exc)
        return report

    # 1) Top-level windows
    try:
        descriptions = adapter.describe_windows()
        summary_lines.append(f"## Top-level windows ({len(descriptions)})")
        summary_lines.extend(f"- {d}" for d in descriptions)
        summary_lines.append("")
    except Exception as exc:  # noqa: BLE001
        summary_lines.append(f"window enumeration failed: {exc!r}")

    # 2) Control dump (main window, then top window as a fallback record)
    try:
        main_dump = adapter.dump_main_window_controls()
        summary_lines.append(f"main-window control dump: {main_dump}")
    except Exception as exc:  # noqa: BLE001
        summary_lines.append(f"main-window control dump failed: {exc!r}")
        try:
            top_dump = adapter.dump_top_window_controls()
            summary_lines.append(f"top-window control dump: {top_dump}")
        except Exception as exc2:  # noqa: BLE001
            summary_lines.append(f"top-window control dump failed: {exc2!r}")

    # 3) Screenshot
    shot = adapter.screenshot_main_window()
    summary_lines.append(f"screenshot: {shot}")

    report = _write_summary(config.reports_dir, session.run_id, summary_lines)
    log.info("Inspection complete. Summary -> %s", report)
    return report


def _write_summary(reports_dir: Path, run_id: str, lines: List[str]) -> Path:
    reports_dir.mkdir(parents=True, exist_ok=True)
    path = reports_dir / f"{run_id}_inspection_summary.md"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def _build_config(args: argparse.Namespace) -> AppConfig:
    config = AppConfig.from_env()
    if args.backend:
        config = config.model_copy(update={"backend": Backend(args.backend)})
    if args.executable:
        config = config.model_copy(update={"executable_path": Path(args.executable)})
    return config


def _parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inspect a running Best Case instance.")
    parser.add_argument(
        "--backend",
        choices=[b.value for b in Backend],
        help="Override the pywinauto backend (uia or win32).",
    )
    parser.add_argument(
        "--executable",
        help="Path to BestCase.exe; if given, the app is started when not running.",
    )
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = _parse_args(argv)
    config = _build_config(args)
    report = run_inspection(config)
    print(f"Inspection summary written to: {report}")
    return 0


def connect_main(argv: Optional[List[str]] = None) -> int:
    """Lightweight 'just connect and list windows' entry point."""
    args = _parse_args(argv)
    config = _build_config(args)
    session = Session.create(config)
    setup_logging(config.logs_dir, level=config.log_level, run_id=session.run_id)
    adapter = BestCaseAdapter(config)
    adapter.connect_or_start()
    for desc in adapter.describe_windows():
        print(desc)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
