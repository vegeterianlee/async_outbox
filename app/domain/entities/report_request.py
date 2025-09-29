from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any


@dataclass
class ReportRequestEntity:
    id: Optional[int]
    requester_email: str
    params: Dict[str, Any]
    job_id: Optional[str]
    result_path: Optional[str]
    error_message: Optional[str]
    created_at: datetime
    updated_at: datetime


