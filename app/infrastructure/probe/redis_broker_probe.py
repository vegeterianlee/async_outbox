import redis.asyncio as aioredis

class RedisBrokerProbe:
    def __init__(self, redis_url: str, queues: list[str] = None):
        self._r = aioredis.from_url(redis_url)
        self._queues = queues or ["celery"]

    async def count_queued(self) -> int:
        total = 0
        for q in self._queues:
            total += int(await self._r.llen(q))
        return total