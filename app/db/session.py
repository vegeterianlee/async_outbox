from typing import AsyncGenerator
import uuid
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.core.config import settings
from app.common.logging.request_id import set_current_request_info, clear_current_request_info


async_engine = create_async_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    future=True,
)

async_session_factory = async_sessionmaker(
    bind=async_engine, expire_on_commit=False, class_=AsyncSession
)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        async_session_id = str(uuid.uuid4())
        set_current_request_info({"async_session_id": async_session_id})
        try:
            yield session
        finally:
            clear_current_request_info()
