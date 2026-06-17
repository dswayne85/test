"""Screenshot helper. Saves timestamped PNGs to the screenshots output folder.

Prefers pywinauto's ``capture_as_image`` for a specific window; falls back to a
full-desktop grab via Pillow's ImageGrab. All imports are lazy.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from ..logging_setup import get_logger

log = get_logger(__name__)


def _timestamped_name(label: str) -> str:
    safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in label)
    return f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{safe}.png"


def capture(
    screenshots_dir: Path,
    label: str = "screenshot",
    window: Optional[Any] = None,
) -> Optional[Path]:
    """Capture ``window`` (a pywinauto wrapper) or the full desktop.

    Returns the saved path, or ``None`` if capture failed (failures are logged,
    never raised, so a screenshot attempt cannot break a flow).
    """
    screenshots_dir.mkdir(parents=True, exist_ok=True)
    target = screenshots_dir / _timestamped_name(label)

    try:
        if window is not None and hasattr(window, "capture_as_image"):
            image = window.capture_as_image()
        else:
            from PIL import ImageGrab  # noqa: WPS433 - lazy, Windows-friendly

            image = ImageGrab.grab()
        image.save(target)
        log.info("Saved screenshot -> %s", target)
        return target
    except Exception as exc:  # noqa: BLE001 - screenshots are best-effort
        log.warning("Screenshot '%s' failed: %r", label, exc)
        return None
