from datetime import datetime

from pydantic import BaseModel, EmailStr
from typing import Any, Dict, Optional

class ReportParams(BaseModel):
    input_number: int

class ReportRequestIn(BaseModel):
    requester_email: EmailStr
    params: ReportParams

class ReportRequestOut(BaseModel):
    id: int
    job_id: Optional[str]
    result_path: Optional[str]
    params: Optional[ReportParams]
    created_at: Optional[datetime]

class ReportStatusOut(BaseModel):
    id: int
    job_id: Optional[str]
    celery_status: Optional[str]
    result_path: Optional[str]
    error_message: Optional[str]


