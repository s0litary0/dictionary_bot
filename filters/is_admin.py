from aiogram import types
from aiogram.filters import Filter

from bot import bot


class IsAdmin(Filter):
    def __init__(self):
        pass 

    async def __call__(self, message: types.Message) -> bool:
        if not hasattr(bot, "admins_list"):
            return False
        return message.from_user.id in bot.admins_list