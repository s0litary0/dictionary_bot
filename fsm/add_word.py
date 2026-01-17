from aiogram.fsm.state import StatesGroup, State


class AddWord(StatesGroup):
    word = State()
    translation = State()