from dataclasses import dataclass
from typing import *  # type: ignore


@dataclass
class Request:
    method: str
    arguments: Dict[str, Any]


@dataclass
class Response:
    result: Any
    error: Optional[str] = None
