from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from bot import bot

command_router = Router(name="commands")


@command_router.message(CommandStart())
async def start_command_handler(message: Message) -> None:
    # print(command_router.name)
    await bot.send_message(chat_id=message.from_user.id, text="Start!")

@command_router.message(Command("help"))
async def help_command_handler(message: Message) -> None:
    await bot.send_contact(chat_id=message.from_user.id, 
                           phone_number="+7 776 286 86 73", 
                           first_name="Sultan")
    # await bot.send_message(chat_id=message.from_user.id,
    #                        text=str(message.chat))
