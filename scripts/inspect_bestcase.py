#!/usr/bin/env python
"""Full inspection: connect, list windows, dump controls, screenshot, report.

Run on the Best Case machine:
    python scripts/inspect_bestcase.py [--backend uia|win32] [--executable PATH]

Try --backend uia first; if controls look empty/opaque, try --backend win32.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from bestcase_agent.flows.inspect_bestcase import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
