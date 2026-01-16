from aiogram import Bot
from dotenv import load_dotenv
from os import getenv

load_dotenv()
print(TOKEN := getenv("TOKEN"))
bot = Bot(TOKEN)