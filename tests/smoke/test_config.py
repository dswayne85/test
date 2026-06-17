"""Smoke tests for the configuration system."""

from __future__ import annotations

from pathlib import Path

from bestcase_agent.config import AppConfig, Backend


def test_defaults() -> None:
    config = AppConfig()
    assert config.backend == Backend.UIA
    assert config.process_name == "BestCase.exe"
    assert config.retry_attempts >= 1
    assert config.connect_timeout > 0


def test_derived_dirs(tmp_path: Path) -> None:
    config = AppConfig(output_dir=tmp_path / "out")
    assert config.logs_dir == tmp_path / "out" / "logs"
    assert config.screenshots_dir == tmp_path / "out" / "screenshots"
    assert config.reports_dir == tmp_path / "out" / "reports"


def test_ensure_dirs_creates_tree(tmp_path: Path) -> None:
    config = AppConfig(output_dir=tmp_path / "out")
    config.ensure_dirs()
    assert config.logs_dir.is_dir()
    assert config.screenshots_dir.is_dir()
    assert config.reports_dir.is_dir()


def test_from_env_reads_environment(monkeypatch) -> None:
    monkeypatch.setenv("BESTCASE_BACKEND", "win32")
    monkeypatch.setenv("BESTCASE_RETRY_ATTEMPTS", "5")
    monkeypatch.setenv("BESTCASE_PROCESS_NAME", "BC.exe")
    config = AppConfig.from_env()
    assert config.backend == Backend.WIN32
    assert config.retry_attempts == 5
    assert config.process_name == "BC.exe"
