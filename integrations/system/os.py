
import os
from typing import Any
from . import abstract


class OsCommand(abstract.Commands):
    def execute(self, command: str) -> tuple[list[dict], Any]:
        result = None
        errors: list[dict] = []
        try:
            result = os.system(command)
        except Exception as exc:
            errors.append({"errors": str(exc), "message": exc.args})
        return errors, result
