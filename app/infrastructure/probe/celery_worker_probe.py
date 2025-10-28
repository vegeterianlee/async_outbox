import asyncio
from app.celery_app import celery_app

"""
    동기 RPC 호출로
    이벤트 루프를 막지 않으려면, 동기 코드를 짧게 다른 스레드 풀에서 실행하고,
    코루틴에서는 await로 결과만 받으면 됨
    루프 블로킹 없이 백그라운드에서 실행하려면 to_thread를 사용하면 됨
"""

# 워커별 작업 리스트 조회 로직 (동기)
"""
insp.active()
{
  "worker1@host": [
      {"name": "dispatch_outbox_events", "id": "abc123", "args": "()", "kwargs": "{}"}
  ],
  "worker2@host": [
      {"name": "generate_report", "id": "xyz456", "args": "()", "kwargs": "{}"},
      {"name": "notify_user", "id": "hij789", "args": "()", "kwargs": "{}"}
  ]
}
"""

def _inspect_sync() -> tuple[int, int, int]:
    insp = celery_app.control.inspect(timeout=1.0)
    active = insp.active() or {} # 현재 실행중인 전체 task 목록
    reserved = insp.reserved() or {} # 대기 중인 전체 task 목록
    scheduled = insp.scheduled() or {} # 예약된 전체 task 목록

    # 워커가 여러개가 있기에 여러 워커들에서의 합계를 구하고자 아래와 같이 설정
    worker_active = sum(len(v or []) for v in (active or {}).values())
    worker_reserved = sum(len(v or []) for v in (reserved or {}).values())
    worker_scheduled = sum(len(v or []) for v in (scheduled or {}).values())
    return worker_active, worker_reserved, worker_scheduled

class CeleryWorkerProbe:
    async def get_counts(self) -> tuple[int, int, int]:
        return await asyncio.to_thread(_inspect_sync)