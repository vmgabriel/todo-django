# Libraries
from dataclasses import dataclass
from abc import ABC, abstractmethod
from pathlib import Path


@dataclass
class Attachment:
    mimetype: str
    path: Path

@dataclass
class Email:
    subject: str
    receivers: list[str]
    body: str
    attachments: list[Attachment]


class EmailSender(ABC):
    @abstractmethod
    def send(self, content: Email):
        raise NotImplementedError()