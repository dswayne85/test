"""Smoke tests: the package and its modules import on any OS.

Critically, importing the adapters/screens must NOT require pywinauto (imports
are lazy). These tests guard that invariant so CI stays green off-Windows.
"""

from __future__ import annotations

import importlib

import pytest

PURE_MODULES = [
    "bestcase_agent",
    "bestcase_agent.config",
    "bestcase_agent.logging_setup",
    "bestcase_agent.runner",
    "bestcase_agent.app.waiters",
    "bestcase_agent.app.keyboard",
    "bestcase_agent.app.screenshots",
    "bestcase_agent.app.selectors",
    "bestcase_agent.app.connect",
    "bestcase_agent.adapters.pywinauto_adapter",
    "bestcase_agent.adapters.bestcase_adapter",
    "bestcase_agent.screens.base_screen",
    "bestcase_agent.screens.main_window",
    "bestcase_agent.screens.case_window",
    "bestcase_agent.screens.creditor_dialog",
    "bestcase_agent.screens.popup_dialog",
    "bestcase_agent.flows.inspect_bestcase",
    "bestcase_agent.flows.add_single_creditor",
    "bestcase_agent.domain.models",
    "bestcase_agent.domain.validators",
    "bestcase_agent.domain.normalizers",
    "bestcase_agent.state.session",
    "bestcase_agent.state.checkpoints",
]


@pytest.mark.parametrize("module_name", PURE_MODULES)
def test_module_imports(module_name: str) -> None:
    assert importlib.import_module(module_name) is not None


def test_version_present() -> None:
    import bestcase_agent

    assert isinstance(bestcase_agent.__version__, str)
