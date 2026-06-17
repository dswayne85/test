"""Keyboard helpers wrapping pywinauto.keyboard.

pywinauto is imported lazily so this module is importable on any platform.
``send_keys`` treats several characters as special ({}()+^%~ etc.); use
:func:`escape` for literal text.
"""

from __future__ import annotations

from ..logging_setup import get_logger

log = get_logger(__name__)

_SPECIAL = set("{}()[]+^%~")


def escape(text: str) -> str:
    """Escape characters that pywinauto's send_keys treats as special."""
    out = []
    for ch in text:
        if ch in _SPECIAL:
            out.append("{" + ch + "}")
        else:
            out.append(ch)
    return "".join(out)


def send_keys(keystrokes: str, *, with_spaces: bool = True, pause: float = 0.02) -> None:
    """Send raw keystrokes (special syntax allowed). Lazy pywinauto import."""
    from pywinauto.keyboard import send_keys as _send_keys  # noqa: WPS433

    log.debug("send_keys: %r", keystrokes)
    _send_keys(keystrokes, with_spaces=with_spaces, pause=pause)


def type_text(text: str, *, pause: float = 0.02) -> None:
    """Type literal text, escaping pywinauto special characters first."""
    send_keys(escape(text), with_spaces=True, pause=pause)
