from django.core.mail.message import EmailMessage
from django.conf import settings
from . import abstract
from logging import getLogger

logger = getLogger(__name__)


class DjangoMail(abstract.EmailSender):
    def send(self, content: abstract.Email):
        email = EmailMessage(
            content.subject,
            content.body,
            settings.EMAIL_HOST_USER,
            content.receivers
        )
        for attachment in content.attachments:
            try:
                email.attach_file(attachment.path, mimetype=attachment.mimetype)
            except Exception as exc:
                logger.error(f"[Django Mail][Error][Attachment] - {exc}")
        email.send()