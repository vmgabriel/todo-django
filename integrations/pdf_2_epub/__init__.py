from enum import Enum
from django.conf import settings
from . import abstract, os


class Pdf2EpubProvider(str, Enum):
    OS = "os"


pdf_2_epub_providers: dict[Pdf2EpubProvider, type[abstract.PDF2EPUB]] = {
    Pdf2EpubProvider.OS: os.OsPDF2EPUB,
}


pdf_2_epub_provider: type[abstract.PDF2EPUB] = pdf_2_epub_providers[settings.PDF_TO_EPUB_PROVIDER]
