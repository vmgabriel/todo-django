from celery import Celery
from celery.utils.log import get_task_logger
from integrations.email import email_provider, Email, Attachment
from django.conf import settings

email_sender = email_provider()
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