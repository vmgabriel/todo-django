from enum import Enum
from django.conf import settings
from . import abstract, os


class Epub2MobiProvider(str, Enum):
    OS = "os"


epub_2_mobi_providers: dict[Epub2MobiProvider, type[abstract.EPUB2Mobi]] = {
    Epub2MobiProvider.OS: os.OsEPUB2Mobi,
}


epub_2_mobi_provider: type[abstract.EPUB2Mobi] = epub_2_mobi_providers[settings.EPUB_TO_MOBI_PROVIDER]
