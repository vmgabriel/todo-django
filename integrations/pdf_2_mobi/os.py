from pathlib import Path

from . import abstract
from integrations import system


class OsPDF2MOBI(abstract.PDF2MOBI):
    def __init__(self):
        self.os: system.abstract.Commands = system.system_provider()
    def execute(self, file: Path) -> Path:
        output_file = str(file.absolute()).replace(".pdf", ".mobi")
        command = "ebook-convert {input} {output}"
        errors_command, _ = self.os.execute(command.format(
            input=str(file.absolute()),
            output=output_file,
        ))
        if errors_command:
            raise Exception(f"[OsPDF2MOBI][Error] - {errors_command}")
        return Path(output_file)