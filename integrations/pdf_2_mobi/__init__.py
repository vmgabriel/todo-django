from enum import Enum
from django.conf import settings
from . import abstract, os


class Pdf2MobiProvider(str, Enum):
    OS = "os"


pdf_2_mobi_providers: dict[Pdf2MobiProvider, type[abstract.PDF2MOBI]] = {
    Pdf2MobiProvider.OS: os.OsPDF2MOBI,
}


pdf_2_mobi_provider: type[abstract.PDF2MOBI] = pdf_2_mobi_providers[settings.PDF_TO_MOBI_PROVIDER]
