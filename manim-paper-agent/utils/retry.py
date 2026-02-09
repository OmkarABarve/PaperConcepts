import time
from typing import Callable, TypeVar

T = TypeVar("T")


def with_retries(fn: Callable[[], T], attempts: int = 3, backoff: float = 1.5, initial_delay: float = 1.0) -> T:
    last_err = None
    delay = initial_delay
    for _ in range(attempts):
        try:
            return fn()
        except Exception as e:
            last_err = e
            time.sleep(delay)
            delay *= backoff
    raise last_err  # type: ignore[misc]

