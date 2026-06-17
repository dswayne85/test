"""Best Case desktop automation agent.

A Windows-only Python agent that automates creditor data entry into Best Case
bankruptcy software using pywinauto.

This top-level package intentionally imports NOTHING that depends on pywinauto,
so it can be imported on any platform. Windows-only behavior lives behind the
adapters/ and screens/ packages and is imported lazily.
"""

from __future__ import annotations

__version__ = "0.1.0"

__all__ = ["__version__"]
