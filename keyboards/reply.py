from aiogram.types import ReplyKeyboardRemove, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


start_keyboard = ReplyKeyboardBuilder()
start_keyboard.add(
    KeyboardButton(text="Список слов 📘"),
    KeyboardButton(text="Добавить новое слово ➕"),
    KeyboardButton(text="Удалить слово ➖"),
)
start_keyboard.adjust(1, 1, 1)

admin_keyboard = ReplyKeyboardBuilder()
admin_keyboard.attach(start_keyboard)
admin_keyboard.row(KeyboardButton(text="Посмотреть пользователей"))

delete_keyboard = ReplyKeyboardRemove()

