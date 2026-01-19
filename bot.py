from os import getenv

from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties


print(TOKEN := getenv("TOKEN"))
bot = Bot(
    token=TOKEN, 
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)

