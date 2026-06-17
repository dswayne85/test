"""Logging configuration: file + console handlers with timestamped log files."""

from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

_LOG_FORMAT = "%(asctime)s | %(levelname)-7s | %(name)s | %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

_configured = False


def setup_logging(
    logs_dir: Path,
    level: str = "INFO",
    run_id: Optional[str] = None,
) -> Path:
    """Configure root logging to console and a timestamped file.

    Returns the path to the created log file. Safe to call more than once;
    handlers are reset on each call so the active run owns the output.
    """
    global _configured

    logs_dir.mkdir(parents=True, exist_ok=True)
    run_id = run_id or datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = logs_dir / f"bestcase_{run_id}.log"

    root = logging.getLogger()
    root.setLevel(getattr(logging, level.upper(), logging.INFO))

    # Remove handlers from any prior configuration so repeated calls are clean.
    for handler in list(root.handlers):
        root.removeHandler(handler)
        handler.close()

    formatter = logging.Formatter(_LOG_FORMAT, datefmt=_DATE_FORMAT)

    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    root.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root.addHandler(console_handler)

    _configured = True
    logging.getLogger(__name__).info("Logging initialized -> %s", log_path)
    return log_path


def get_logger(name: str) -> logging.Logger:
    """Return a module logger (configuring a basic console fallback if needed)."""
    if not _configured and not logging.getLogger().handlers:
        logging.basicConfig(level=logging.INFO, format=_LOG_FORMAT, datefmt=_DATE_FORMAT)
    return logging.getLogger(name)
