"""JSON checkpointing so batch runs can resume without re-entering creditors.

Not used by Milestone 1 flows, but defined now so the single-entry path can
record progress and the future batch executor can resume cleanly.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class Checkpoint:
    """Tracks which creditors in a job have been entered."""

    job_name: str
    completed_keys: List[str] = field(default_factory=list)
    failed_keys: List[str] = field(default_factory=list)
    updated_at: Optional[str] = None

    def mark_completed(self, key: str) -> None:
        if key not in self.completed_keys:
            self.completed_keys.append(key)
        if key in self.failed_keys:
            self.failed_keys.remove(key)
        self.updated_at = datetime.now().isoformat(timespec="seconds")

    def mark_failed(self, key: str) -> None:
        if key not in self.failed_keys:
            self.failed_keys.append(key)
        self.updated_at = datetime.now().isoformat(timespec="seconds")

    def is_completed(self, key: str) -> bool:
        return key in self.completed_keys


def save_checkpoint(checkpoint: Checkpoint, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(asdict(checkpoint), indent=2), encoding="utf-8")
    return path


def load_checkpoint(path: Path) -> Optional[Checkpoint]:
    if not path.exists():
        return None
    data: Dict[str, object] = json.loads(path.read_text(encoding="utf-8"))
    return Checkpoint(
        job_name=str(data.get("job_name", "")),
        completed_keys=list(data.get("completed_keys", [])),  # type: ignore[arg-type]
        failed_keys=list(data.get("failed_keys", [])),  # type: ignore[arg-type]
        updated_at=data.get("updated_at"),  # type: ignore[arg-type]
    )
