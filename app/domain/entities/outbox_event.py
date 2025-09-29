from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any


class OutboxStatus(str, Enum):
    pending = "pending"
    dispatched = "dispatched"
    failed = "failed"


@dataclass
class OutboxEventEntity:
    id: Optional[int]
    aggregate_type: str
    aggregate_id: str
    event_type: str
    payload: Dict[str, Any]
    status: OutboxStatus
    attempts: int
    last_error: Optional[str]
    created_at: datetime
    dispatched_at: Optional[datetime]


