"""Unit tests for validators and the Creditor/CreditorJob models."""

from __future__ import annotations

from decimal import Decimal
from pathlib import Path

import pytest
from pydantic import ValidationError

from bestcase_agent.domain import validators as val
from bestcase_agent.domain.models import Creditor, CreditorJob


def test_state_and_zip_validators() -> None:
    assert val.is_valid_state("IL")
    assert val.is_valid_state("il")
    assert not val.is_valid_state("ZZ")
    assert val.is_valid_zip("60601")
    assert val.is_valid_zip("60601-1234")
    assert not val.is_valid_zip("6060")


def test_validate_creditor_fields_collects_errors() -> None:
    errors = val.validate_creditor_fields(
        name="",
        address_line1="",
        city="",
        state="ZZ",
        zip_code="bad",
        amount=Decimal("-1"),
    )
    assert len(errors) == 6


def test_creditor_normalizes_and_validates() -> None:
    creditor = Creditor(
        name="  Acme   Collections  ",
        address_line1="123 Main St",
        city="Springfield",
        state="il",
        zip="627010000",
        account_number="  ACME-1  ",
        amount="$1,250.75",
    )
    assert creditor.name == "Acme Collections"
    assert creditor.state == "IL"
    assert creditor.zip_code == "62701-0000"
    assert creditor.account_number == "ACME-1"
    assert creditor.amount == Decimal("1250.75")
    assert creditor.amount_str() == "1250.75"


def test_creditor_rejects_invalid() -> None:
    with pytest.raises(ValidationError):
        Creditor(
            name="",
            address_line1="x",
            city="y",
            state="ZZ",
            zip="00000-",
            amount="0",
        )


def test_creditor_job_loads_from_fixture(small_job_path: Path) -> None:
    job = CreditorJob.from_json_file(small_job_path)
    assert job.case_name == "Sample Debtor 2026"
    assert len(job.creditors) == 2
    first, second = job.creditors
    assert first.state == "IL"
    assert first.zip_code == "62701-0000"
    assert first.amount == Decimal("1250.75")
    assert second.account_number == "4455-2210"
    assert second.amount == Decimal("8400")
