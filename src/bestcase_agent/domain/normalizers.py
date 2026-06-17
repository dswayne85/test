"""Pure normalization helpers for creditor data.

No external dependencies — trivially unit-testable on any platform.
"""

from __future__ import annotations

import re
from decimal import Decimal, InvalidOperation
from typing import Optional

_WHITESPACE_RE = re.compile(r"\s+")
_NON_DIGIT_RE = re.compile(r"\D")
_CURRENCY_STRIP_RE = re.compile(r"[^0-9.\-]")


def normalize_whitespace(value: Optional[str]) -> str:
    """Trim and collapse internal whitespace to single spaces."""
    if value is None:
        return ""
    return _WHITESPACE_RE.sub(" ", value).strip()


def normalize_state(value: Optional[str]) -> str:
    """Uppercase a 2-letter US state code (best effort).

    Leaves longer values trimmed/uppercased so callers can validate separately.
    """
    cleaned = normalize_whitespace(value).upper()
    return cleaned


def normalize_zip(value: Optional[str]) -> str:
    """Normalize a US ZIP to ``#####`` or ``#####-####`` when possible."""
    digits = _NON_DIGIT_RE.sub("", value or "")
    if len(digits) == 9:
        return f"{digits[:5]}-{digits[5:]}"
    if len(digits) == 5:
        return digits
    # Return collapsed original (trimmed) when it does not look like a US ZIP.
    return normalize_whitespace(value)


def normalize_account_number(value: Optional[str]) -> str:
    """Trim and collapse whitespace; preserve characters (some accounts have dashes)."""
    return normalize_whitespace(value)


def parse_amount(value: object) -> Decimal:
    """Parse a currency-ish value into a Decimal.

    Accepts Decimal/int/float/str like ``"$1,234.56"``. Raises ValueError on
    anything unparseable.
    """
    if isinstance(value, Decimal):
        return value
    if isinstance(value, (int, float)):
        return Decimal(str(value))
    if isinstance(value, str):
        cleaned = _CURRENCY_STRIP_RE.sub("", value)
        if cleaned in ("", "-", ".", "-."):
            raise ValueError(f"Cannot parse amount from {value!r}")
        try:
            return Decimal(cleaned)
        except InvalidOperation as exc:
            raise ValueError(f"Cannot parse amount from {value!r}") from exc
    raise ValueError(f"Unsupported amount type: {type(value)!r}")


def format_amount(value: Decimal) -> str:
    """Format a Decimal as a plain two-decimal string (e.g. ``1234.56``)."""
    return f"{value.quantize(Decimal('0.01'))}"
