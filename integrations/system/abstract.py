from typing import Any
from abc import ABC, abstractmethod


class Commands(ABC):
    @abstractmethod
    def execute(self, command: str) -> tuple[list[dict], Any]:
        raise NotImplementedError