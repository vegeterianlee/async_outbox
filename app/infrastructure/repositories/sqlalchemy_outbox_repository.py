from typing import Sequence
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from app.domain.entities.outbox_event import OutboxEventEntity, OutboxStatus
from app.domain.repositories.outbox_repository import OutboxRepository
from app.models.outbox import OutboxEvent


def _to_entity(row: OutboxEvent) -> OutboxEventEntity:
    return OutboxEventEntity(
        id=row.id,
        aggregate_type=row.aggregate_type,
        aggregate_id=row.aggregate_id,
        event_type=row.event_type,
        payload=row.payload,
        status=OutboxStatus(row.status),
        attempts=row.attempts,
        last_error=row.last_error,
        created_at=row.created_at,
        dispatched_at=row.dispatched_at,
    )


class SqlAlchemyOutboxRepository(OutboxRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, event: OutboxEventEntity) -> OutboxEventEntity:
        row = OutboxEvent(
            aggregate_type=event.aggregate_type,
            aggregate_id=event.aggregate_id,
            event_type=event.event_type,
            payload=event.payload,
        )
        self._session.add(row)
        await self._session.flush()
        return _to_entity(row)

    async def list_pending(self, limit: int = 100) -> Sequence[OutboxEventEntity]:
        result = await self._session.scalars(
            select(OutboxEvent).where(OutboxEvent.status == OutboxStatus.pending.value).order_by(OutboxEvent.id.asc()).limit(limit)
        )
        return [_to_entity(r) for r in result.all()]

    async def mark_dispatched(self, event_id: int) -> None:
        await self._session.execute(
            update(OutboxEvent)
            .where(OutboxEvent.id == event_id)
            .values(status=OutboxStatus.dispatched.value, dispatched_at=datetime.utcnow())
        )

    async def mark_failed(self, event_id: int, error: str) -> None:
        await self._session.execute(
            update(OutboxEvent)
            .where(OutboxEvent.id == event_id)
            .values(status=OutboxStatus.failed.value, attempts=OutboxEvent.attempts + 1, last_error=error)
        )


