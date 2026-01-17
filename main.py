import asyncio

from aiogram import Dispatcher, types

from bot import bot
from routers.user_private import user_private_router
from routers.admin_private import admin_private_router
from routers.user_group import user_group_router
from common.bot_commands_list import private_commands

ALLOWED_UPDATES = [
    "message",
    "edited_message"
]

dispatcher = Dispatcher()
dispatcher.include_routers(user_private_router, admin_private_router, user_group_router)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private_commands, scope=types.BotCommandScopeAllPrivateChats())
    await dispatcher.start_polling(bot, allowed_updates=ALLOWED_UPDATES) 

if __name__ == "__main__":
    asyncio.run(main(), debug=True)