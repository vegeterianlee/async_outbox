from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import settings

_engine = None
_session_factory = None

@asynccontextmanager
async def get_session():
    global _engine, _session_factory
    if _engine is None:
        _engine = create_async_engine(settings.DATABASE_URL, pool_pre_ping=True, future=True)
        _session_factory = async_sessionmaker(bind=_engine, expire_on_commit=False, class_=AsyncSession)
    session = _session_factory()
    try:
        yield session
    finally:
        await session.close()