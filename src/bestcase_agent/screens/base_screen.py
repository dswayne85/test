"""Base class for screen/page objects."""

from __future__ import annotations

from typing import Any

from ..app.selectors import Selector
from ..app.waiters import wait_until
from ..config import AppConfig
from ..logging_setup import get_logger

log = get_logger(__name__)


class BaseScreen:
    """Common behavior for screen objects.

    A screen wraps a pywinauto window spec (``self.window``) and resolves
    :class:`Selector` objects into control wrappers against it.
    """

    def __init__(self, window: Any, config: AppConfig) -> None:
        self.window = window
        self.config = config

    # -- control resolution ------------------------------------------------
    def control(self, selector: Selector) -> Any:
        """Return the pywinauto control spec for ``selector`` on this window."""
        return self.window.child_window(**selector.as_kwargs())

    def exists(self, selector: Selector, timeout: float = 1.0) -> bool:
        try:
            return bool(self.control(selector).exists(timeout=timeout))
        except Exception:  # noqa: BLE001
            return False

    def wait_visible(self, selector: Selector, timeout: float | None = None) -> Any:
        """Wait until a control is visible, then return its wrapper object."""
        timeout = self.config.action_timeout if timeout is None else timeout
        ctrl = self.control(selector)
        wait_until(
            lambda: ctrl.exists() and ctrl.is_visible(),
            timeout=timeout,
            description=f"selector {selector.name!r} visible",
        )
        return ctrl.wrapper_object()

    def set_edit_text(self, selector: Selector, value: str) -> None:
        """Set the text of an edit control (clears first)."""
        ctrl = self.wait_visible(selector)
        ctrl.set_edit_text("")
        ctrl.set_edit_text(value)
        log.debug("Set %s = %r", selector.name, value)

    def click(self, selector: Selector) -> None:
        ctrl = self.wait_visible(selector)
        ctrl.click_input()
        log.debug("Clicked %s", selector.name)
