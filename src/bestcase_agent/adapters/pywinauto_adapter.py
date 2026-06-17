"""Generic pywinauto adapter: start/connect, enumerate windows, dump controls.

This class is intentionally Best-Case-agnostic. Best Case specifics live in
``bestcase_adapter.BestCaseAdapter`` which composes this one.

pywinauto is imported lazily inside methods so the module imports on any OS.
"""

from __future__ import annotations

import io
from contextlib import redirect_stdout
from datetime import datetime
from pathlib import Path
from typing import Any, List, Optional

from ..app import connect as _connect
from ..config import AppConfig, Backend
from ..logging_setup import get_logger

log = get_logger(__name__)


class PywinautoAdapter:
    """Wraps a single pywinauto ``Application`` instance."""

    def __init__(self, backend: Backend) -> None:
        self.backend = backend
        self._app: Optional[Any] = None

    # -- lifecycle ---------------------------------------------------------
    @property
    def app(self) -> Any:
        if self._app is None:
            raise RuntimeError("Not connected. Call start() or connect() first.")
        return self._app

    def is_connected(self) -> bool:
        return self._app is not None

    def start(self, executable_path: Path, timeout: float = 30.0) -> "PywinautoAdapter":
        self._app = _connect.start_application(executable_path, self.backend, timeout)
        return self

    def connect(
        self,
        *,
        process_name: Optional[str] = None,
        title_re: Optional[str] = None,
        timeout: float = 30.0,
    ) -> "PywinautoAdapter":
        self._app = _connect.connect_application(
            self.backend,
            process_name=process_name,
            title_re=title_re,
            timeout=timeout,
        )
        return self

    # -- discovery ---------------------------------------------------------
    def top_windows(self) -> List[Any]:
        """Return wrapper objects for all top-level windows of the process."""
        windows = self.app.windows()
        log.info("Enumerated %d top-level window(s).", len(windows))
        return list(windows)

    def describe_windows(self) -> List[str]:
        """Return human-readable 'title [class]' descriptions of top windows."""
        descriptions: List[str] = []
        for win in self.top_windows():
            try:
                title = win.window_text()
            except Exception:  # noqa: BLE001
                title = "<no title>"
            try:
                cls = win.class_name()
            except Exception:  # noqa: BLE001
                cls = "<no class>"
            descriptions.append(f"{title!r} [{cls}]")
        return descriptions

    def window(self, **criteria: Any) -> Any:
        """Return a window spec from the connected app (``app.window(**crit)``)."""
        return self.app.window(**criteria)

    def dump_controls(
        self,
        report_dir: Path,
        *,
        title_re: Optional[str] = None,
        depth: Optional[int] = None,
        label: str = "controls",
    ) -> Path:
        """Run ``print_control_identifiers`` and write the output to a text file.

        If ``title_re`` is given, dump that window; otherwise dump the app's
        top window. Returns the path to the written report.
        """
        report_dir.mkdir(parents=True, exist_ok=True)
        target = (
            report_dir
            / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{label}.txt"
        )

        if title_re is not None:
            spec = self.app.window(title_re=title_re)
        else:
            spec = self.app.top_window()

        buffer = io.StringIO()
        header = f"# Control dump (backend={self.backend.value}) title_re={title_re!r}\n"
        try:
            with redirect_stdout(buffer):
                spec.print_control_identifiers(depth=depth)
        except Exception as exc:  # noqa: BLE001
            buffer.write(f"\n!! print_control_identifiers failed: {exc!r}\n")
            log.warning("Control dump for %r failed: %r", title_re, exc)

        target.write_text(header + buffer.getvalue(), encoding="utf-8")
        log.info("Wrote control dump -> %s", target)
        return target

    @classmethod
    def from_config(cls, config: AppConfig) -> "PywinautoAdapter":
        return cls(backend=config.backend)
