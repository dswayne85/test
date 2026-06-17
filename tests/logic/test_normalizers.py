"""Unit tests for pure normalization helpers."""

from __future__ import annotations

from decimal import Decimal

import pytest

from bestcase_agent.domain import normalizers as norm


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("  hello   world  ", "hello world"),
        ("tabs\tand\nnewlines", "tabs and newlines"),
        (None, ""),
        ("single", "single"),
    ],
)
def test_normalize_whitespace(raw, expected) -> None:
    assert norm.normalize_whitespace(raw) == expected


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("il", "IL"),
        ("  ca ", "CA"),
        ("Tx", "TX"),
    ],
)
def test_normalize_state(raw, expected) -> None:
    assert norm.normalize_state(raw) == expected


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("627010000", "62701-0000"),
        ("60601", "60601"),
        ("60601-1234", "60601-1234"),
        ("not a zip", "not a zip"),
    ],
)
def test_normalize_zip(raw, expected) -> None:
    assert norm.normalize_zip(raw) == expected


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("$1,250.75", Decimal("1250.75")),
        (8400, Decimal("8400")),
        (12.5, Decimal("12.5")),
        ("  2,000  ", Decimal("2000")),
        (Decimal("3.33"), Decimal("3.33")),
    ],
)
def test_parse_amount(raw, expected) -> None:
    assert norm.parse_amount(raw) == expected


@pytest.mark.parametrize("bad", ["", "abc", "$", "-."])
def test_parse_amount_rejects_garbage(bad) -> None:
    with pytest.raises(ValueError):
        norm.parse_amount(bad)


def test_format_amount() -> None:
    assert norm.format_amount(Decimal("1250.7")) == "1250.70"
    assert norm.format_amount(Decimal("8400")) == "8400.00"
