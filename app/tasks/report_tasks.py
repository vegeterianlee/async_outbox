import csv
import os
from datetime import datetime

from app.celery_app import celery_app
from app.db.session import async_session_factory
from app.infrastructure.uow.sqlalchemy_uow import SqlAlchemyUnitOfWork


@celery_app.task(name="generate_report", bind=True)
def generate_report(self, report_id: int, params: dict) -> str:
    """
    sleep 없이 에라토스테네스의 체를 이용해 소수를 계산하는 로직
    탐색 범위를 제곱근 이하로 설정할 수 있지만, 전체를 탐색하게 하여 시간 복잡도를 더 키웠음
    - Updates Celery state periodically with PROGRESS.
    - CSV columns: input_n, prime_count.
    """
    try:
        n = int(params.get("n", 5_000_000))  # choose a large default; tune per environment
    except Exception:  # noqa: BLE001
        n = 5_000_000
    if n < 100_000:
        n = 100_000

    # Less-optimized sieve variant (counts divisors for every number)
    # Numbers with exactly 2 divisors are primes.
    num_arr = [0] * (n + 1)
    step_report = max(1, n // 20)  # ~5% progress increments
    for i in range(1, n + 1):
        for j in range(i, n + 1, i):
            num_arr[j] += 1
        if (i % step_report) == 0 or i == n:
            progress = int((i / n) * 100)
            self.update_state(state="PROGRESS", meta={"progress": progress})

    prime_count = sum(1 for k in range(2, n + 1) if num_arr[k] == 2)

    # Generate CSV and persist result path
    import asyncio
    return asyncio.run(_finalize_report_async(report_id, n, prime_count))


async def _finalize_report_async(report_id: int, n: int, prime_count: int) -> str:
    # Write minimal CSV with input and answer
    os.makedirs("/app/data", exist_ok=True)
    file_path = f"/app/data/report_{report_id}_{int(datetime.utcnow().timestamp())}.csv"

    with open(file_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["input_n", "prime_count"])
        writer.writerow([n, prime_count])

    # persist result path
    async with async_session_factory() as session:
        uow = SqlAlchemyUnitOfWork(session)
        await uow.reports.set_result(report_id, file_path)
        await uow.commit()

    return file_path


