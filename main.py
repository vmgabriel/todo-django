"""Telegram Connection"""

# Libraries
import telebot
from time import sleep
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser, InputPeerChannel
from telethon import TelegramClient, sync, events

# Modules
from django.conf import settings


client = TelegramClient('session', settings.TELEGRAM_API_ID, settings.TELEGRAM_API_HASH)


if not client.is_user_authorized():
    client.send_code_request(settings.PHONE_DEFAULT)
    client.sign_in(settings.PHONE_DEFAULT, input('Enter the code: '))


def send_message(message: str, phone_destiny: str):
    client.connect()
    try:
        contact = client.get_entity(phone_destiny)
        client.send_message(contact, message)
    except Exception as e:
        print(e)
    client.disconnect()
