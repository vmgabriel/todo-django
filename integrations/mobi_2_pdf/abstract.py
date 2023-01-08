from abc import ABC, abstractmethod
from pathlib import Path


class MOBI2PDF(ABC):
    @abstractmethod
    def execute(self, file: Path) -> Path:
        raise NotImplementedError