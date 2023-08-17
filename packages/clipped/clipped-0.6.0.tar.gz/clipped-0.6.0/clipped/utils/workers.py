import asyncio
import logging
import os
import signal
import threading

from contextlib import asynccontextmanager, contextmanager
from typing import Generator, Optional

_logger = logging.getLogger("clipped.workers")


def get_pool_workers() -> int:
    return min(32, (os.cpu_count() or 1) + 4)


def get_core_workers(per_core: int, max_workers: Optional[int] = None) -> int:
    count = per_core * (os.cpu_count() or 1) + 1
    return max(count, max_workers) if max_workers else count


def _exit_context(exit_event):
    def _exit_handler(*args, **kwargs):
        _logger.info("Keyboard Interrupt received, exiting pool.")
        exit_event.set()

    original = signal.getsignal(signal.SIGINT)
    try:
        signal.signal(signal.SIGINT, _exit_handler)
        yield exit_event
    except SystemExit:
        pass
    finally:
        signal.signal(signal.SIGINT, original)

@contextmanager
def sync_exit_context() -> Generator:
    exit_event = threading.Event()

    yield _exit_context(exit_event)


@asynccontextmanager
async def async_exit_context() -> Generator:
    exit_event = asyncio.Event()

    yield _exit_context(exit_event)


def get_wait(current: int) -> float:
    intervals = [0.25, 0.5, 1.0, 2.0, 4.0, 8.0]

    if current >= 5:
        current = 5
    return intervals[current]
