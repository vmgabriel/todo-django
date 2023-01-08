from pathlib import Path

from . import abstract
from integrations import system


class OsEPUB2PDF(abstract.EPUB2PDF):
    def __init__(self):
        self.os: system.abstract.Commands = system.system_provider()
    def execute(self, file: Path) -> Path:
        output_file = str(file.absolute()).replace(".epub", ".pdf")
        command = "ebook-convert {input} {output}"
        errors_command, _ = self.os.execute(command.format(
            input=str(file.absolute()),
            output=output_file,
        ))
        if errors_command:
            raise Exception(f"[OsEPUB2PDF][Error ] - {errors_command}")
        return Path(output_file)