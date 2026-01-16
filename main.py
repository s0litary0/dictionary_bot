import asyncio
from bot import bot
from aiogram import Dispatcher
from routers.commands import command_router


dispatcher = Dispatcher()
dispatcher.include_routers(command_router)

async def main():
    await dispatcher.start_polling(bot) 


if __name__ == "__main__":
    asyncio.run(main(), debug=True)