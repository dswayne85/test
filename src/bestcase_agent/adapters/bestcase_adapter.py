"""Best Case-specific adapter built on top of :class:`PywinautoAdapter`.

Responsible for connecting to Best Case using config-driven title/process
patterns, locating the main and case windows, and exposing them to screens.

Most window-finding here relies on regex title patterns from AppConfig, which
must be tuned after the first inspection run.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, List, Optional

from ..config import AppConfig
from ..logging_setup import get_logger
from .pywinauto_adapter import PywinautoAdapter

log = get_logger(__name__)


class BestCaseAdapter:
    """High-level entry point for talking to Best Case."""

    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self.pwa = PywinautoAdapter(backend=config.backend)

    # -- connection --------------------------------------------------------
    def connect_or_start(self) -> "BestCaseAdapter":
        """Connect to a running instance, or start one if an exe path is set.

        Milestone 1 expects Best Case to already be running, so we try connect
        first and only start as a fallback when ``executable_path`` is set.
        """
        try:
            self.pwa.connect(
                process_name=self.config.process_name,
                title_re=self.config.main_window_title_re,
                timeout=self.config.connect_timeout,
            )
            log.info("Connected to running Best Case.")
            return self
        except Exception as exc:  # noqa: BLE001
            log.warning("Connect failed (%r).", exc)
            if self.config.executable_path:
                log.info("Falling back to starting Best Case from configured path.")
                self.pwa.start(
                    self.config.executable_path, timeout=self.config.connect_timeout
                )
                return self
            raise

    # -- windows -----------------------------------------------------------
    def main_window(self) -> Any:
        """Return the Best Case main window spec (by configured title regex)."""
        return self.pwa.window(title_re=self.config.main_window_title_re)

    def case_window(self) -> Any:
        """Return the case/editor window spec. TODO: confirm title after inspection."""
        return self.pwa.window(title_re=self.config.case_window_title_re)

    def creditor_dialog(self) -> Any:
        """Return the creditor dialog spec. TODO: confirm title after inspection."""
        return self.pwa.window(title_re=self.config.creditor_dialog_title_re)

    def describe_windows(self) -> List[str]:
        return self.pwa.describe_windows()

    def dump_main_window_controls(self, label: str = "main_window") -> Path:
        return self.pwa.dump_controls(
            self.config.reports_dir,
            title_re=self.config.main_window_title_re,
            label=label,
        )

    def dump_top_window_controls(self, label: str = "top_window") -> Path:
        return self.pwa.dump_controls(self.config.reports_dir, label=label)

    def screenshot_main_window(self) -> Optional[Path]:
        from ..app.screenshots import capture  # noqa: WPS433 - lazy

        try:
            window = self.main_window().wrapper_object()
        except Exception as exc:  # noqa: BLE001
            log.warning("Could not resolve main window for screenshot: %r", exc)
            window = None
        return capture(self.config.screenshots_dir, label="main_window", window=window)
