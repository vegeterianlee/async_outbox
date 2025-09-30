from typing import Optional
from pydantic import BaseModel

class SimpleTaskMetricsOut(BaseModel):
    total_requests: int
    queued_now: int
    processing_now: int
    completed_success: int  # 누적(성공)
