"""Telegram Connection"""

# Libraries
import telebot
import asyncio
from time import sleep
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser, InputPeerChannel
from telethon import TelegramClient, sync, events

# Modules
from django.conf import settings


# if not client.is_user_authorized():
#     client.send_code_request(settings.PHONE_DEFAULT)
#     client.sign_in(settings.PHONE_DEFAULT, input('Enter the code: '))


def send_message(message: str, phone_destiny: str):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    client = TelegramClient('session', settings.TELEGRAM_API_ID, settings.TELEGRAM_API_HASH, loop=loop)
    client.connect()
    try:
        contact = client.get_entity(phone_destiny)
        client.send_message(contact, message)
    except Exception as e:
        print(e)
    client.disconnect()

