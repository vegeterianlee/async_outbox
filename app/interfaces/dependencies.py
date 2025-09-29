from typing import Callable
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_async_session
from app.infrastructure.uow.sqlalchemy_uow import SqlAlchemyUnitOfWork

async def uow_factory(session: AsyncSession) -> SqlAlchemyUnitOfWork:
    return SqlAlchemyUnitOfWork(session)


def provide_uow_factory() -> Callable[[], SqlAlchemyUnitOfWork]:
    async def _factory() -> SqlAlchemyUnitOfWork:
        # get_async_session is a FastAPI dependency generator; here we call it directly
        # in route we will inject session and pass to the UoW instead for clarity.
        raise RuntimeError("Use route-level dependency to pass session to uow factory")

    return _factory


