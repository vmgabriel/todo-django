from abc import ABC, abstractmethod
from pathlib import Path


class PDF2EPUB(ABC):
    @abstractmethod
    def execute(self, file: Path) -> Path:
        raise NotImplementedError