from abc import ABC, abstractmethod
from pathlib import Path


class EPUB2Mobi(ABC):
    @abstractmethod
    def execute(self, file: Path) -> Path:
        raise NotImplementedError