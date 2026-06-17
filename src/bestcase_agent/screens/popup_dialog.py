"""Generic popup/confirmation dialog handling.

Best Case (like most Windows apps) raises modal popups for confirmations,
warnings, and errors. Handling them generically keeps flows resilient.

STUB: button titles are placeholders pending inspection.
"""

from __future__ import annotations

from typing import Iterable

from .base_screen import BaseScreen
from ..app.selectors import Selector
from ..logging_setup import get_logger

log = get_logger(__name__)

# Common affirmative/negative button captions to try. Extend after inspection.
AFFIRMATIVE_TITLES = ("OK", "Yes", "Save", "Continue")
NEGATIVE_TITLES = ("Cancel", "No", "Close")


class PopupDialog(BaseScreen):
    """A modal popup with one or more buttons."""

    def _click_first_available(self, titles: Iterable[str]) -> bool:
        for title in titles:
            selector = Selector(name=f"popup_{title}", criteria={"title": title})
            if self.exists(selector, timeout=0.5):
                self.click(selector)
                log.info("Dismissed popup via %r button.", title)
                return True
        return False

    def accept(self) -> bool:
        """Click the first affirmative button found. Returns True if clicked."""
        return self._click_first_available(AFFIRMATIVE_TITLES)

    def dismiss(self) -> bool:
        """Click the first negative button found. Returns True if clicked."""
        return self._click_first_available(NEGATIVE_TITLES)
