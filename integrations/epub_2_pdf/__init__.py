from enum import Enum
from django.conf import settings
from . import abstract, os


class Epub2PdfProvider(str, Enum):
    OS = "os"


epub_2_pdf_providers: dict[Epub2PdfProvider, type[abstract.EPUB2PDF]] = {
    Epub2PdfProvider.OS: os.OsEPUB2PDF,
}


epub_2_pdf_provider: type[abstract.EPUB2PDF] = epub_2_pdf_providers[settings.EPUB_TO_PDF_PROVIDER]
