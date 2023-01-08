from enum import Enum
from django.conf import settings
from . import abstract, os


class Mobi2PdfProvider(str, Enum):
    OS = "os"


mobi_2_pdf_providers: dict[Mobi2PdfProvider, type[abstract.MOBI2PDF]] = {
    Mobi2PdfProvider.OS: os.OsMOBI2PDF,
}


mobi_2_pdf_provider: type[abstract.MOBI2PDF] = mobi_2_pdf_providers[settings.MOBI_TO_PDF_PROVIDER]
