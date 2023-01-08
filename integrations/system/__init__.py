from enum import Enum
from django.conf import settings
from . import abstract, os

class SystemProvider(str, Enum):
    OS = "os"


system_providers: dict[SystemProvider, type[abstract.Commands]] = {
    SystemProvider.OS: os.OsCommand,
}


system_provider: type[abstract.Commands] = system_providers[settings.SYSTEM_PROVIDER]
