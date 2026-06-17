"""Best Case add/edit creditor dialog.

This is the heart of the single-creditor flow. Field interactions are wired to
placeholder selectors in app/selectors.py — replace those auto_ids/titles with
real ones from the inspection dump, then this screen should work largely as-is.
"""

from __future__ import annotations

from .base_screen import BaseScreen
from ..app import selectors as sel
from ..domain.models import Creditor
from ..logging_setup import get_logger

log = get_logger(__name__)


class CreditorDialog(BaseScreen):
    """The dialog used to enter a single creditor's data."""

    def fill(self, creditor: Creditor) -> None:
        """Populate the dialog fields from a validated :class:`Creditor`.

        Uses placeholder selectors. Once real selectors are in place, this
        should enter data without further changes. Fields that the dialog does
        not expose can simply have their lines removed.
        """
        log.info("Filling creditor dialog for %r", creditor.name)
        self.set_edit_text(sel.CREDITOR_NAME, creditor.name)
        self.set_edit_text(sel.CREDITOR_ADDRESS1, creditor.address_line1)
        if creditor.address_line2:
            self.set_edit_text(sel.CREDITOR_ADDRESS2, creditor.address_line2)
        self.set_edit_text(sel.CREDITOR_CITY, creditor.city)
        self.set_edit_text(sel.CREDITOR_STATE, creditor.state)
        self.set_edit_text(sel.CREDITOR_ZIP, creditor.zip_code)
        if creditor.account_number:
            self.set_edit_text(sel.CREDITOR_ACCOUNT_NUMBER, creditor.account_number)
        self.set_edit_text(sel.CREDITOR_AMOUNT, creditor.amount_str())

    def save(self) -> None:
        """Click the save/OK button. TODO: confirm selector + any confirmation popup."""
        self.click(sel.SAVE_BUTTON)

    def cancel(self) -> None:
        self.click(sel.CANCEL_BUTTON)
