from celery import Celery
from celery.utils.log import get_task_logger
from django.conf import settings
from integrations.email import email_provider, Email, Attachment
from integrations.pdf_2_epub import pdf_2_epub_provider
from integrations.epub_2_pdf import  epub_2_pdf_provider
from integrations.mobi_2_pdf import mobi_2_pdf_provider
from integrations.pdf_2_mobi import pdf_2_mobi_provider
from integrations.epub_2_mobi import epub_2_mobi_provider
from integrations.mobi_2_epub import mobi_2_epub_provider
from . import models

email_sender = email_provider()
pdf_2_epub_conversor = pdf_2_epub_provider()
epub_2_pdf_conversor = epub_2_pdf_provider()
epub_2_mobi_conversor = epub_2_mobi_provider()
mobi_2_pdf_conversor = mobi_2_pdf_provider()
pdf_2_mobi_conversor = pdf_2_mobi_provider()
mobi_2_epub_conversor = mobi_2_epub_provider()
logger = get_task_logger(__name__)


def get_mimetype(name_file: str) -> str:
    mime: str = ""
    frm = name_file.split(".")[-1].lower()
    if frm == "pdf":
        mime = "application/pdf"
    if frm == "mobi":
        mime = "application/x-mobipocket-ebook"
    if frm == "epub":
        mime = "application/epub+zip"
    if not mime:
        raise Exception("Format Not Valid")
    return mime


@Celery().task(name='send_book')
def send_book(receivers: list[str], book_name_file: str):
    attach = Attachment(
        path=settings.PATH_BOOKS / book_name_file,
        mimetype=get_mimetype(book_name_file),
    )
    to_send = Email(
        subject=settings.BOOK_SEND_EMAIL_SUBJECT,
        body=settings.BOOK_SEND_EMAIL_BODY,
        receivers=receivers,
        attachments=[attach],
    )
    email_sender.send(to_send)


def convert_pdf_to_epub(book_name_file: str) -> str:
    print(f"convert_pdf_to_epub ")
    file = settings.PATH_BOOKS / book_name_file
    pdf_2_epub_conversor.execute(file)
    return "books/" + book_name_file.replace(".pdf", ".epub")


def convert_epub_to_pdf(book_name_file: str) -> str:
    print(f"convert_epub_to_pdf ")
    file = settings.PATH_BOOKS / book_name_file
    epub_2_pdf_conversor.execute(file)
    return "books/" + book_name_file.replace(".epub", ".pdf")


def convert_mobi_to_pdf(book_name_file: str) -> str:
    print(f"convert_mobi_to_pdf ")
    file = settings.PATH_BOOKS / book_name_file
    mobi_2_pdf_conversor.execute(file)
    return "books/" + book_name_file.replace(".mobi", ".pdf")


def convert_pdf_to_mobi(book_name_file: str) -> str:
    print(f"convert_pdf_to_mobi ")
    file = settings.PATH_BOOKS / book_name_file
    pdf_2_mobi_conversor.execute(file)
    return "books/" + book_name_file.replace(".mobi", ".pdf")


def convert_epub_to_mobi(book_name_file: str) -> str:
    print(f"convert_epub_to_mobi ")
    file = settings.PATH_BOOKS / book_name_file
    epub_2_mobi_conversor.execute(file)
    return "books/" + book_name_file.replace(".epub", ".mobi")


def convert_mobi_to_epub(book_name_file: str) -> str:
    print(f"convert_mobi_to_epub ")
    file = settings.PATH_BOOKS / book_name_file
    mobi_2_epub_conversor.execute(file)
    return "books/" + book_name_file.replace(".mobi", ".epub")


to_call = lambda input: lambda output: f"convert_{input}_to_{output}"


@Celery().task(name='convert_book')
def conversion_book(book_id: int):
    book: models.Books = models.Books.objects.get(id=book_id)
    book.progress_conversion = models.ProgressConversion.IN_PROGRESS
    book.save()
    book_name_file = book.file.name.split("/")[-1]

    pdf_url = None
    epub_url = None
    mobi_url = None
    current_format = book_name_file.split(".")[-1]
    if current_format == "pdf":
        pdf_url = book.file.name
    if current_format == "epub":
        epub_url = book.file.name
    if current_format == "mobi":
        mobi_url = book.file.name

    try:
        to_assigned_input = to_call(current_format)
        pdf_url = pdf_url or globals()[to_assigned_input("pdf")](book_name_file)
        epub_url = epub_url or globals()[to_assigned_input("epub")](book_name_file)
        mobi_url = mobi_url or globals()[to_assigned_input("mobi")](book_name_file)

        book.file = pdf_url
        book.file_epub = epub_url
        book.file_mobi = mobi_url
        book.progress_conversion = models.ProgressConversion.SUCCESS
    except Exception as exc:
        book.progress_conversion = models.ProgressConversion.FAIL
        logger.error(exc)
    book.save()