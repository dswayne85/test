"""Explicit waits and retry wrappers.

Pure Python — no pywinauto. Use these instead of blind ``time.sleep`` calls so
flows are reliable and self-documenting.
"""

from __future__ import annotations

import functools
import time
from typing import Callable, Optional, Tuple, Type, TypeVar

from ..logging_setup import get_logger

log = get_logger(__name__)

T = TypeVar("T")


class WaitTimeout(TimeoutError):
    """Raised when :func:`wait_until` exceeds its timeout."""


def wait_until(
    predicate: Callable[[], bool],
    timeout: float,
    interval: float = 0.5,
    description: str = "condition",
) -> None:
    """Poll ``predicate`` until it returns truthy or ``timeout`` elapses.

    Raises :class:`WaitTimeout` on expiry.
    """
    deadline = time.monotonic() + timeout
    last_error: Optional[Exception] = None
    while time.monotonic() < deadline:
        try:
            if predicate():
                return
        except Exception as exc:  # noqa: BLE001 - predicate may probe a not-yet-ready UI
            last_error = exc
        time.sleep(interval)
    msg = f"Timed out after {timeout}s waiting for {description}."
    if last_error is not None:
        msg += f" Last error: {last_error!r}"
    raise WaitTimeout(msg)


def retry(
    attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: Tuple[Type[BaseException], ...] = (Exception,),
    description: Optional[str] = None,
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Decorator: retry a callable on ``exceptions`` with exponential backoff."""

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args: object, **kwargs: object) -> T:
            label = description or func.__name__
            current_delay = delay
            last_exc: Optional[BaseException] = None
            for attempt in range(1, attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as exc:  # type: ignore[misc]
                    last_exc = exc
                    if attempt >= attempts:
                        break
                    log.warning(
                        "Attempt %d/%d for %s failed (%r); retrying in %.1fs",
                        attempt,
                        attempts,
                        label,
                        exc,
                        current_delay,
                    )
                    time.sleep(current_delay)
                    current_delay *= backoff
            raise RuntimeError(
                f"{label} failed after {attempts} attempts"
            ) from last_exc

        return wrapper

    return decorator
