from os import getenv
from dotenv import load_dotenv

from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties


load_dotenv()
print(TOKEN := getenv("TOKEN"))
bot = Bot(
    token=TOKEN, 
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)

