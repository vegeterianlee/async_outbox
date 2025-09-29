from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import String, Integer, DateTime, JSON, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class OutboxStatus(str, Enum):
    pending = "pending"
    dispatched = "dispatched"
    failed = "failed"


class OutboxEvent(Base):
    __tablename__ = 'outbox_events'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # Aggregate root reference (e.g., user id)
    aggregate_type: Mapped[str] = mapped_column(String(50), nullable=False)
    aggregate_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)

    # Event details
    event_type: Mapped[str] = mapped_column(String(100), nullable=False)
    payload: Mapped[dict] = mapped_column(JSON, nullable=False)

    status: Mapped[str] = mapped_column(String(20), default=OutboxStatus.pending.value, index=True)
    attempts: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    last_error: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
    dispatched_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)


