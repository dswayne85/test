"""Centralized configuration for the Best Case agent.

Configuration is loaded from environment variables (optionally via a local
``.env`` file). Nothing here imports pywinauto, so it is safe on any platform.
"""

from __future__ import annotations

import os
from enum import Enum
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseModel, Field, field_validator


class Backend(str, Enum):
    """Supported pywinauto backends."""

    UIA = "uia"
    WIN32 = "win32"


def _env(name: str, default: Optional[str] = None) -> Optional[str]:
    value = os.environ.get(name)
    if value is None or value.strip() == "":
        return default
    return value.strip()


class AppConfig(BaseModel):
    """Runtime configuration for a single agent session.

    Build it with :meth:`from_env`, which reads a ``.env`` file if present.
    """

    # Connection / process
    executable_path: Optional[Path] = None
    process_name: str = "BestCase.exe"
    backend: Backend = Backend.UIA

    # Window-title regex patterns. TUNE THESE AFTER THE FIRST INSPECTION RUN.
    main_window_title_re: str = r".*Best Case.*"
    case_window_title_re: str = r".*Case.*"
    creditor_dialog_title_re: str = r".*Creditor.*"

    # Timing / retries (seconds)
    connect_timeout: float = 30.0
    action_timeout: float = 15.0
    retry_attempts: int = 3
    retry_delay: float = 1.0

    # Output
    output_dir: Path = Path("output")
    log_level: str = "INFO"

    model_config = {"arbitrary_types_allowed": True}

    @field_validator("output_dir", "executable_path", mode="before")
    @classmethod
    def _coerce_path(cls, value: object) -> object:
        if value is None or value == "":
            return None if value in (None, "") else value
        if isinstance(value, str):
            return Path(value)
        return value

    # Derived artifact directories -----------------------------------------
    @property
    def logs_dir(self) -> Path:
        return self.output_dir / "logs"

    @property
    def screenshots_dir(self) -> Path:
        return self.output_dir / "screenshots"

    @property
    def reports_dir(self) -> Path:
        return self.output_dir / "reports"

    def ensure_dirs(self) -> None:
        """Create the output directory tree if it does not yet exist."""
        for directory in (self.logs_dir, self.screenshots_dir, self.reports_dir):
            directory.mkdir(parents=True, exist_ok=True)

    @classmethod
    def from_env(cls, dotenv_path: Optional[Path] = None) -> "AppConfig":
        """Load configuration from environment / ``.env``."""
        load_dotenv(dotenv_path=dotenv_path, override=False)

        exe = _env("BESTCASE_EXECUTABLE_PATH")
        return cls(
            executable_path=Path(exe) if exe else None,
            process_name=_env("BESTCASE_PROCESS_NAME", "BestCase.exe"),
            backend=Backend(_env("BESTCASE_BACKEND", "uia")),
            main_window_title_re=_env("BESTCASE_MAIN_WINDOW_TITLE_RE", r".*Best Case.*"),
            case_window_title_re=_env("BESTCASE_CASE_WINDOW_TITLE_RE", r".*Case.*"),
            creditor_dialog_title_re=_env(
                "BESTCASE_CREDITOR_DIALOG_TITLE_RE", r".*Creditor.*"
            ),
            connect_timeout=float(_env("BESTCASE_CONNECT_TIMEOUT", "30")),
            action_timeout=float(_env("BESTCASE_ACTION_TIMEOUT", "15")),
            retry_attempts=int(_env("BESTCASE_RETRY_ATTEMPTS", "3")),
            retry_delay=float(_env("BESTCASE_RETRY_DELAY", "1.0")),
            output_dir=Path(_env("BESTCASE_OUTPUT_DIR", "output")),
            log_level=_env("BESTCASE_LOG_LEVEL", "INFO"),
        )
