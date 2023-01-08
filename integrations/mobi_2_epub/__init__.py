from enum import Enum
from django.conf import settings
from . import abstract, os


class Mobi2PdfProvider(str, Enum):
    OS = "os"


mobi_2_epub_providers: dict[Mobi2PdfProvider, type[abstract.MOBI2EPUB]] = {
    Mobi2PdfProvider.OS: os.OsMOBI2EPUB,
}


mobi_2_epub_provider: type[abstract.MOBI2EPUB] = mobi_2_epub_providers[settings.MOBI_TO_PDF_PROVIDER]
