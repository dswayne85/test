"""Structured, validated business models for creditor data.

Uses pydantic v2. Construction normalizes inputs and enforces validation rules,
so any ``Creditor`` instance is safe to feed to the entry flow.
"""

from __future__ import annotations

from decimal import Decimal
from pathlib import Path
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from . import normalizers as norm
from . import validators as val


class Creditor(BaseModel):
    """A single creditor record to be entered into Best Case."""

    model_config = ConfigDict(str_strip_whitespace=True)

    name: str
    address_line1: str
    address_line2: Optional[str] = None
    city: str
    state: str
    zip_code: str = Field(alias="zip")
    account_number: Optional[str] = None
    amount: Decimal = Decimal("0.00")
    classification: Optional[str] = Field(
        default=None,
        description="e.g. 'unsecured', 'secured', 'priority'. Free text for now.",
    )

    # -- normalization (runs before validation) ----------------------------
    @field_validator("name", "address_line1", "address_line2", "city", mode="before")
    @classmethod
    def _clean_text(cls, value: object) -> object:
        if value is None:
            return value
        return norm.normalize_whitespace(str(value))

    @field_validator("state", mode="before")
    @classmethod
    def _clean_state(cls, value: object) -> object:
        return norm.normalize_state(str(value)) if value is not None else value

    @field_validator("zip_code", mode="before")
    @classmethod
    def _clean_zip(cls, value: object) -> object:
        return norm.normalize_zip(str(value)) if value is not None else value

    @field_validator("account_number", mode="before")
    @classmethod
    def _clean_account(cls, value: object) -> object:
        if value is None:
            return value
        return norm.normalize_account_number(str(value))

    @field_validator("amount", mode="before")
    @classmethod
    def _clean_amount(cls, value: object) -> object:
        if value is None or value == "":
            return Decimal("0.00")
        return norm.parse_amount(value)

    # -- cross-field validation --------------------------------------------
    @model_validator(mode="after")
    def _validate_business_rules(self) -> "Creditor":
        errors = val.validate_creditor_fields(
            name=self.name,
            address_line1=self.address_line1,
            city=self.city,
            state=self.state,
            zip_code=self.zip_code,
            amount=self.amount,
        )
        if errors:
            raise ValueError("; ".join(errors))
        return self

    # -- helpers -----------------------------------------------------------
    def amount_str(self) -> str:
        return norm.format_amount(self.amount)


class CreditorJob(BaseModel):
    """A batch job: metadata plus a list of creditors to enter into one case."""

    model_config = ConfigDict(str_strip_whitespace=True)

    case_name: str
    creditors: List[Creditor] = Field(default_factory=list)

    @classmethod
    def from_json_file(cls, path: Path) -> "CreditorJob":
        """Load and validate a job from a JSON file."""
        return cls.model_validate_json(Path(path).read_text(encoding="utf-8"))
