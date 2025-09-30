import asyncio
from app.celery_app import celery_app

"""
    동기 RPC 호출로
    이벤트 루프를 막지 않으려면, 동기 코드를 짧게 다른 스레드 풀에서 실행하고,
    코루틴에서는 await로 결과만 받으면 됨
    루프 블로킹 없이 백그라운드에서 실행하려면 to_thread를 사용하면 됨
"""

# 워커별 작업 리스트 조회 로직 (동기)
def _inspect_sync() -> tuple[int, int, int]:
    insp = celery_app.control.inspect(timeout=1.0)
    active = insp.active() or {}
    reserved = insp.reserved() or {}
    scheduled = insp.scheduled() or {}
    worker_active = sum(len(v or []) for v in (active or {}).values())
    worker_reserved = sum(len(v or []) for v in (reserved or {}).values())
    worker_scheduled = sum(len(v or []) for v in (scheduled or {}).values())
    return worker_active, worker_reserved, worker_scheduled

class CeleryWorkerProbe:
    async def get_counts(self) -> tuple[int, int, int]:
        return await asyncio.to_thread(_inspect_sync)