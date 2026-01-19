import asyncio

from dotenv import load_dotenv
load_dotenv()
from aiogram import Dispatcher, types

from bot import bot
from routers.user_private import user_private_router
from routers.admin_private import admin_private_router
from routers.user_group import user_group_router
from common.bot_commands_list import private_commands
from database.engine import create_db, drop_db, session_maker
from middleware.db import DatabaseSession

# ALLOWED_UPDATES = [
#     "message",
#     "edited_message",
#     "callback_query"
# ]

dispatcher = Dispatcher()
dispatcher.include_routers(user_private_router, admin_private_router, user_group_router)

async def on_startup():
    # await drop_db()
    await create_db()

async def main():
    dispatcher.startup.register(on_startup)

    dispatcher.message.middleware(DatabaseSession(session_pool=session_maker))
    dispatcher.callback_query.middleware(DatabaseSession(session_pool=session_maker))

    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private_commands, scope=types.BotCommandScopeAllPrivateChats())
    await dispatcher.start_polling(bot, 
                                   allowed_updates=dispatcher.resolve_used_update_types()
                                   ) 

if __name__ == "__main__":
    asyncio.run(main(), debug=True)