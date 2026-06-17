"""Validation helpers for creditor data.

These return lists of human-readable error strings (empty == valid), which is
convenient for batch reporting. The pydantic model in models.py enforces the
same rules at construction time.
"""

from __future__ import annotations

import re
from decimal import Decimal
from typing import List

# A small set; expand to all US states/territories as needed.
US_STATES = {
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID",
    "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS",
    "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK",
    "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV",
    "WI", "WY", "DC", "PR", "VI", "GU", "AS", "MP",
}

_ZIP_RE = re.compile(r"^\d{5}(?:-\d{4})?$")


def is_valid_state(state: str) -> bool:
    return state.upper() in US_STATES


def is_valid_zip(zip_code: str) -> bool:
    return bool(_ZIP_RE.match(zip_code or ""))


def validate_creditor_fields(
    *,
    name: str,
    address_line1: str,
    city: str,
    state: str,
    zip_code: str,
    amount: Decimal,
) -> List[str]:
    """Return a list of validation errors (empty list == valid)."""
    errors: List[str] = []
    if not name or not name.strip():
        errors.append("name is required")
    if not address_line1 or not address_line1.strip():
        errors.append("address_line1 is required")
    if not city or not city.strip():
        errors.append("city is required")
    if not is_valid_state(state):
        errors.append(f"state {state!r} is not a valid 2-letter US state code")
    if not is_valid_zip(zip_code):
        errors.append(f"zip_code {zip_code!r} is not a valid US ZIP")
    if amount < Decimal("0"):
        errors.append("amount must not be negative")
    return errors
