import asyncio
from threading import Thread
from typing import Awaitable, TypeVar, Optional

R = TypeVar("R")

class _SingleEventLoop:
    def __init__(self) -> None:
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._thread: Optional[Thread] = None

    def _ensure_loop(self) -> None:
        if self._loop and self._loop.is_running():
            return
        def _run():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            self._loop = loop
            loop.run_forever()
        self._thread = Thread(target=_run, daemon=True)
        self._thread.start()

    def run(self, coro: Awaitable[R]) -> R:
        self._ensure_loop()
        fut = asyncio.run_coroutine_threadsafe(coro, self._loop)  # type: ignore[arg-type]
        return fut.result()

single_loop = _SingleEventLoop()

def run_in_single_loop(coro: Awaitable[R]) -> R:
    return single_loop.run(coro)