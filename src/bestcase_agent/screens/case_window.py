"""Best Case case/editor window.

STUB: actions are placeholders pending the first inspection run.
"""

from __future__ import annotations

from .base_screen import BaseScreen
from ..logging_setup import get_logger

log = get_logger(__name__)


class CaseWindow(BaseScreen):
    """The window where an individual case is edited."""

    def add_new_creditor(self) -> None:
        """Trigger the 'add creditor' action to open the creditor dialog.

        TODO: implement after inspection (button, menu, or toolbar action).
        """
        raise NotImplementedError(
            "add_new_creditor: wire after inspecting the case window controls."
        )
