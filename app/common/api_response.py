from typing import Optional, Any, TypeVar, Generic
from pydantic import BaseModel
from app.common.logging.request_id import get_current_request_info

T = TypeVar("T")
class ApiResponse(BaseModel ,Generic[T]):
    request_id: Optional[str] = None
    success: bool
    data: Optional[T] = None
    code: int = 200


def api_response(
    data: Optional[Any] = None,
    code: int = 200,
    success: bool = True,
):
    request_id = get_current_request_info().get("async_session_id", "empty_async_session_id")
    return ApiResponse(
        request_id=request_id,
        success=success,
        data=data,
        code=code,
    ).model_dump()


