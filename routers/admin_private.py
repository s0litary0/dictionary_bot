from aiogram import Router, types, F
from aiogram.filters import Command

from filters import ChatTypeFilter, IsAdmin
from keyboards import admin_keyboard


admin_private_router = Router(name="admin_private")
admin_private_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())


@admin_private_router.message(Command("admin"))
async def admin_command(message: types.Message):
    await message.answer(f"Привет, админ {message.from_user.first_name}", 
                         reply_markup=admin_keyboard.as_markup(
                             resize_keyboard=True,
                             input_field_placeholder="Выберите действие..."
                         ))
    
@admin_private_router.message(Command("list users"))
@admin_private_router.message(F.text.lower() == "посмотреть пользователей")
async def list_users_command(message: types.Message):
    await message.answer("Вот все юзеры")