from aiogram import Bot, Router, types
from aiogram.filters import Command

from filters import ChatTypeFilter


user_group_router = Router(name="user_group")
user_group_router.message.filter(ChatTypeFilter(["group"]))


@user_group_router.message(Command("admin"))
async def get_admins_list(message: types.Message, bot: Bot):
    chat_id = message.chat.id
    admins_list = await bot.get_chat_administrators(chat_id)
    await message.answer(str(admins_list))

    admins_list = [
        member.user.id for member in admins_list
        if member.status in "creator administrator"
    ]
    bot.admins_list = admins_list
    # if message.from_user.id in admins_list:
    #     await message.delete()