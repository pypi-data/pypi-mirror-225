from abc import ABC, abstractmethod
from typing import *  # type: ignore


__all__ = [
    "Transport",
]


class Transport(ABC):
    @abstractmethod
    async def invoke(self, method: str, arguments: Dict[str, Any]) -> Any:
        raise NotImplementedError()

    @abstractmethod
    async def receive(self) -> Tuple[str, Dict[str, Any]]:
        raise NotImplementedError()
