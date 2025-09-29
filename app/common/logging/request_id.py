from contextvars import ContextVar
from typing import Dict, Any

_request_info: ContextVar[Dict[str, Any]] = ContextVar("request_info", default={})


def set_current_request_info(info: Dict[str, Any]) -> None:
    current = _request_info.get().copy()
    current.update(info)
    _request_info.set(current)


def get_current_request_info() -> Dict[str, Any]:
    return _request_info.get()


def clear_current_request_info() -> None:
    _request_info.set({})


