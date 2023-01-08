# Libraries
from enum import Enum
from django.conf import settings
from . import (
    abstract as email_abstract,
    django_email,
)
from .abstract import Email, Attachment


class EmailProvider(str, Enum):
    DJANGO_EMAIL = "django_email"


email_providers: dict[EmailProvider, type[email_abstract.EmailSender]] = {
    EmailProvider.DJANGO_EMAIL: django_email.DjangoMail,
}

email_provider: type[email_abstract.EmailSender] = email_providers[settings.EMAIL_PROVIDER]
