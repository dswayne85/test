"""Per-run session metadata."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from ..config import AppConfig


@dataclass
class Session:
    """Identifies a single agent run and where its artifacts live."""

    run_id: str
    started_at: datetime
    config: AppConfig

    @classmethod
    def create(cls, config: AppConfig) -> "Session":
        config.ensure_dirs()
        now = datetime.now()
        return cls(run_id=now.strftime("%Y%m%d_%H%M%S"), started_at=now, config=config)

    @property
    def reports_dir(self) -> Path:
        return self.config.reports_dir

    @property
    def screenshots_dir(self) -> Path:
        return self.config.screenshots_dir

    @property
    def logs_dir(self) -> Path:
        return self.config.logs_dir
