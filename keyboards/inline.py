from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_callback_btns(
    *,
    btns: dict[str, str],
    sizes: tuple[int] = (2, )
):
    keyboard = InlineKeyboardBuilder()

    for btn, data in btns.items():
        keyboard.add(InlineKeyboardButton(text=btn, callback_data=data))
    keyboard.adjust(*sizes)

    return keyboard.as_markup()