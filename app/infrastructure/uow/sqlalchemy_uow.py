from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.uow import UnitOfWork
from app.infrastructure.repositories.sqlalchemy_outbox_repository import SqlAlchemyOutboxRepository
from app.infrastructure.repositories.sqlalchemy_report_repository import SqlAlchemyReportRepository


class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self.outbox = SqlAlchemyOutboxRepository(session)
        self.reports = SqlAlchemyReportRepository(session)

    async def __aenter__(self) -> "SqlAlchemyUnitOfWork":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        if exc:
            await self._session.rollback()
        else:
            await self._session.commit()

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()


