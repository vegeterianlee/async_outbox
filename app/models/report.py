from datetime import datetime
from typing import Optional

from sqlalchemy import String, Integer, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


class ReportRequest(Base):
    __tablename__ = 'report_requests'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    requester_email: Mapped[str] = mapped_column(String(255), nullable=False)
    params: Mapped[dict] = mapped_column(JSON, nullable=False)

    # Queue에 쌓였을 시, 저장되는 백그라운드 job id
    job_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)

    # 결과 메타데이터
    result_path: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


