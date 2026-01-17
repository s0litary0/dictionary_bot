from aiogram import Router, types
from aiogram import F
from aiogram.filters import CommandStart, Command, or_f, StateFilter
from aiogram.utils.formatting import as_list, Bold
from aiogram.fsm.context import FSMContext

from filters import ChatTypeFilter
from keyboards import start_keyboard, delete_keyboard
from fsm import AddWord

user_private_router = Router(name="user_private")
user_private_router.message.filter(ChatTypeFilter(["private"]))

@user_private_router.message(CommandStart())
async def start_command(message: types.Message):
    await message.answer("start",
                         reply_markup=start_keyboard.as_markup(
                             resize_keyboard=True,
                             input_field_placeholder="Выберите действие"
                         ))

@user_private_router.message(Command("help"))
async def help_command(message: types.Message):
    await message.answer(Bold("help").as_html())

@user_private_router.message(or_f(Command("menu"), F.text.casefold() == "меню"))
async def menu_command(message: types.Message):
    await message.answer(Bold("menu").as_html())

@user_private_router.message(or_f(Command("list"), F.text.casefold() == "список слов 📘"))
async def list_command(message: types.Message):
    await message.answer(Bold("list").as_html())

# fsm add word

@user_private_router.message(StateFilter(None), or_f(Command("add_word"), F.text.casefold() == "добавить новое слово ➕"))
async def add_word_command(message: types.Message, state: FSMContext):
    await message.answer(
        Bold("Введите слово:").as_html(), 
        reply_markup=delete_keyboard
    )  
    await state.set_state(AddWord.word)

@user_private_router.message(StateFilter("*"), Command("cancel"))
@user_private_router.message(StateFilter("*"), F.text.casefold() == "отмена")
async def cancel_command(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == None:
        return
    await state.clear()
    await message.answer(Bold("Действия отменены").as_html())

@user_private_router.message(AddWord.word, F.text)
async def add_word(message: types.Message, state: FSMContext):
    if len(message.text) > 20: 
        await message.answer("Длина слов не может превышать 20 символов! Попробуйте еще раз.")
        return
    
    await state.update_data(word=message.text.casefold())
    await message.answer(Bold("Введите перевод: ").as_html())
    await state.set_state(AddWord.translation)

@user_private_router.message(AddWord.word)
async def add_word_error(message: types.Message):
    await message.answer("Неправильный тип ввода, пожалуйста введите текст!")

@user_private_router.message(AddWord.translation, F.text)
async def add_translation(message: types.Message, state: FSMContext):
    if len(message.text) > 20: 
        await message.answer("Длина слов не может превышать 20 символов! Попробуйте еще раз.")
        return

    await state.update_data(translation=message.text.casefold())
    await message.answer(
        Bold("Слово успешно добавлено!").as_html(), 
        reply_markup=start_keyboard.as_markup(
            resize_keyboard=True,
            input_field_placeholder="Выберите действие"
        )
    )
    data = await state.get_data()
    await message.answer(str(data))
    await state.clear()

@user_private_router.message(AddWord.translation)
async def add_translation_error(message: types.Message):
    await message.answer("Неправильный тип ввода, пожалуйста введите текст!")


@user_private_router.message(or_f(Command("delete_word"), F.text.lower() == "удалить слово ➖"))
async def delete_word_command(message: types.Message):
    await message.answer(Bold("delete").as_html())  

