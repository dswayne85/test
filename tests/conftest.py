"""Pytest configuration / shared fixtures."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

# Ensure src/ is importable even if the package is not installed.
SRC = Path(__file__).resolve().parent.parent / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

FIXTURES = Path(__file__).resolve().parent / "fixtures"


@pytest.fixture
def fixtures_dir() -> Path:
    return FIXTURES


@pytest.fixture
def small_job_path() -> Path:
    return FIXTURES / "creditors_small.json"
