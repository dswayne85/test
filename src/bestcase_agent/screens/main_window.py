"""Best Case main application window.

STUB: navigation actions are placeholders pending the first inspection run.
"""

from __future__ import annotations

from .base_screen import BaseScreen
from ..logging_setup import get_logger

log = get_logger(__name__)


class MainWindow(BaseScreen):
    """The top-level Best Case window."""

    def open_case(self, case_name: str) -> None:
        """Open/select a case by name.

        TODO: implement after inspection. Likely a menu navigation or a list
        selection in the case manager. Capture the control identifiers for the
        case list / open-case menu first.
        """
        raise NotImplementedError("open_case: wire after inspecting Best Case main window.")

    def open_creditor_section(self) -> None:
        """Navigate to the creditors/Schedule D-F section of the open case.

        TODO: implement after inspection.
        """
        raise NotImplementedError(
            "open_creditor_section: wire after inspecting the case window."
        )
