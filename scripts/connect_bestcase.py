#!/usr/bin/env python
"""Connect to a running Best Case instance and list its top-level windows.

Run on the Best Case machine:
    python scripts/connect_bestcase.py [--backend uia|win32] [--executable PATH]
"""

from __future__ import annotations

import sys
from pathlib import Path

# Allow running directly from a checkout without installing the package.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from bestcase_agent.flows.inspect_bestcase import connect_main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(connect_main(sys.argv[1:]))
