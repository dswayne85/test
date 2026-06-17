"""Single source of truth for Best Case window/control selectors.

Per the project rules, selectors live HERE and in screens/*.py only — never
scattered across flows or adapters. Most values below are placeholders to be
filled in after the first inspection run (see flows/inspect_bestcase.py).

A :class:`Selector` is a backend-agnostic bag of pywinauto ``child_window``
criteria (title, auto_id, control_type, class_name, ...). Adapters/screens
expand it into the actual pywinauto call.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class Selector:
    """A reusable, named set of pywinauto ``child_window`` criteria."""

    name: str
    criteria: Dict[str, Any] = field(default_factory=dict)
    note: Optional[str] = None

    def as_kwargs(self) -> Dict[str, Any]:
        """Return criteria suitable for ``window.child_window(**kwargs)``."""
        return dict(self.criteria)


# ---------------------------------------------------------------------------
# Window-level selectors (title patterns also live in AppConfig as regex).
# ---------------------------------------------------------------------------

MAIN_WINDOW = Selector(
    name="main_window",
    criteria={"title_re": r".*Best Case.*"},
    note="TODO: confirm exact main window title after inspection.",
)

CASE_WINDOW = Selector(
    name="case_window",
    criteria={"title_re": r".*Case.*"},
    note="TODO: confirm case/editor window title after inspection.",
)

CREDITOR_DIALOG = Selector(
    name="creditor_dialog",
    criteria={"title_re": r".*Creditor.*"},
    note="TODO: confirm the add/edit creditor dialog title after inspection.",
)

# ---------------------------------------------------------------------------
# Creditor dialog field selectors — ALL PLACEHOLDERS.
# Replace auto_id/title/control_type once dump_controls output is available.
# ---------------------------------------------------------------------------

CREDITOR_NAME = Selector(
    name="creditor_name",
    criteria={"auto_id": "TODO_NAME", "control_type": "Edit"},
    note="TODO: creditor name edit field.",
)

CREDITOR_ADDRESS1 = Selector(
    name="creditor_address1",
    criteria={"auto_id": "TODO_ADDRESS1", "control_type": "Edit"},
    note="TODO: address line 1 edit field.",
)

CREDITOR_ADDRESS2 = Selector(
    name="creditor_address2",
    criteria={"auto_id": "TODO_ADDRESS2", "control_type": "Edit"},
    note="TODO: address line 2 edit field.",
)

CREDITOR_CITY = Selector(
    name="creditor_city",
    criteria={"auto_id": "TODO_CITY", "control_type": "Edit"},
    note="TODO: city edit field.",
)

CREDITOR_STATE = Selector(
    name="creditor_state",
    criteria={"auto_id": "TODO_STATE", "control_type": "Edit"},
    note="TODO: state edit/combo field.",
)

CREDITOR_ZIP = Selector(
    name="creditor_zip",
    criteria={"auto_id": "TODO_ZIP", "control_type": "Edit"},
    note="TODO: ZIP edit field.",
)

CREDITOR_ACCOUNT_NUMBER = Selector(
    name="creditor_account_number",
    criteria={"auto_id": "TODO_ACCOUNT", "control_type": "Edit"},
    note="TODO: account number edit field.",
)

CREDITOR_AMOUNT = Selector(
    name="creditor_amount",
    criteria={"auto_id": "TODO_AMOUNT", "control_type": "Edit"},
    note="TODO: claim amount edit field.",
)

SAVE_BUTTON = Selector(
    name="save_button",
    criteria={"title": "TODO_SAVE", "control_type": "Button"},
    note="TODO: save/OK button on the creditor dialog.",
)

CANCEL_BUTTON = Selector(
    name="cancel_button",
    criteria={"title": "TODO_CANCEL", "control_type": "Button"},
    note="TODO: cancel button on the creditor dialog.",
)
