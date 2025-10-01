import asyncio
import os
from threading import Thread, Event
from typing import Awaitable, TypeVar, Optional

R = TypeVar("R")

class _SingleEventLoop:
    def __init__(self) -> None:
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._thread: Optional[Thread] = None
        self._ready = Event()
        # prefork PID 가드
        self._pid = os.getpid()
        if hasattr(os, "register_at_fork"):
            os.register_at_fork(after_in_child=self._reset)

    def _reset(self) -> None:
        self._loop = None
        self._thread = None
        self._ready = Event()
        self._pid = os.getpid()

    def _run_loop(self) -> None:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        self._loop = loop
        # 준비 완료 신호
        self._ready.set()
        loop.run_forever()

    def init(self, timeout: float = 2.0) -> None:
        if self._pid != os.getpid():
            self._reset()

        if self._loop and self._loop.is_running():
            return
        self._ready.clear()
        self._thread = Thread(target=self._run_loop, daemon=True)
        self._thread.start()
        if not self._ready.wait(timeout=timeout):
            raise RuntimeError("failed to start background event loop")
        if not (self._loop and self._loop.is_running()):
            raise RuntimeError("event loop not running after start")

    def run(self, coro: Awaitable[R]) -> R:
        # 제출 전 반드시 대기
        self.init()
        fut = asyncio.run_coroutine_threadsafe(coro, self._loop)
        return fut.result()

single_loop = _SingleEventLoop()

def run_in_single_loop(coro: Awaitable[R]) -> R:
    return single_loop.run(coro)