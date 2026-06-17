"""Thin functional wrappers around pywinauto's Application start/connect.

All pywinauto imports are lazy. Higher-level code should prefer
``adapters.bestcase_adapter.BestCaseAdapter`` which uses these.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

from ..config import Backend
from ..logging_setup import get_logger

log = get_logger(__name__)


class ConnectionError_(RuntimeError):
    """Raised when starting or connecting to Best Case fails."""


def make_application(backend: Backend) -> Any:
    """Return a fresh pywinauto ``Application`` for the given backend."""
    from pywinauto.application import Application  # noqa: WPS433 - lazy

    return Application(backend=backend.value)


def start_application(
    executable_path: Path,
    backend: Backend,
    timeout: float = 30.0,
) -> Any:
    """Start Best Case from ``executable_path`` and return the Application."""
    from pywinauto.application import Application  # noqa: WPS433 - lazy

    exe = Path(executable_path)
    if not exe.exists():
        raise ConnectionError_(f"Best Case executable not found: {exe}")
    log.info("Starting Best Case: %s (backend=%s)", exe, backend.value)
    try:
        app = Application(backend=backend.value).start(str(exe), timeout=timeout)
    except Exception as exc:  # noqa: BLE001
        raise ConnectionError_(f"Failed to start Best Case at {exe}: {exc!r}") from exc
    return app


def connect_application(
    backend: Backend,
    *,
    process_name: Optional[str] = None,
    title_re: Optional[str] = None,
    timeout: float = 30.0,
) -> Any:
    """Connect to a running Best Case instance.

    Tries by window ``title_re`` first (most reliable across restarts), then
    falls back to ``process_name`` (path image). Raises
    :class:`ConnectionError_` if neither succeeds.
    """
    from pywinauto.application import Application  # noqa: WPS433 - lazy

    app = Application(backend=backend.value)
    errors = []

    if title_re:
        try:
            log.info("Connecting by title_re=%r (backend=%s)", title_re, backend.value)
            app.connect(title_re=title_re, timeout=timeout)
            return app
        except Exception as exc:  # noqa: BLE001
            errors.append(f"title_re={title_re!r}: {exc!r}")

    if process_name:
        try:
            log.info("Connecting by path=%r (backend=%s)", process_name, backend.value)
            app.connect(path=process_name, timeout=timeout)
            return app
        except Exception as exc:  # noqa: BLE001
            errors.append(f"path={process_name!r}: {exc!r}")

    raise ConnectionError_(
        "Could not connect to a running Best Case instance. "
        "Is it open? Tried: " + "; ".join(errors)
    )
