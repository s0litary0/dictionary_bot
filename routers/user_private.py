import traceback

from aiogram import Router, types
from aiogram import F
from aiogram.filters import CommandStart, Command, or_f, StateFilter
from aiogram.utils.formatting import as_numbered_list, Bold, Text, as_list
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from filters import ChatTypeFilter
from keyboards import start_keyboard, delete_keyboard
from keyboards.inline import get_callback_btns
from fsm import AddWord
from database.orm_query import (orm_add_word_translation,
                                 orm_get_all_words_translations,
                                 orm_delete_word_translation)

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
    await message.answer(
        as_list(
            Bold("Простой бот для отслжеивания изучаемых слов."),
            "Список доступных команд: ",
            as_numbered_list(
                *["/list", "/add_word", "/delete_word"]
            ),
            sep="\n\n"
        ).as_html()
    )

@user_private_router.message(or_f(Command("menu"), F.text.casefold() == "меню"))
async def menu_command(message: types.Message):
    await message.answer(Bold("menu").as_html())

# list words
@user_private_router.message(or_f(Command("list"), F.text.casefold() == "список слов 📘"))
async def list_command(message: types.Message, session: AsyncSession):
    try:
        words_list = await orm_get_all_words_translations(session)

        if not words_list:
            await message.answer("Список пуст")
            return

        await message.answer(
            as_numbered_list(
                *[f"{word_translation.word} - {word_translation.translation}" 
                  for word_translation in words_list]
            ).as_html()
        )
    except Exception as e:
        print(traceback.print_exc())
        await message.answer(
            f"Error {e}"
        )
        

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
    if message.text.startswith("/"):
        await message.answer("Команды пока не доступны.")
    
    await state.update_data(word=message.text.casefold())
    await message.answer(Bold("Введите перевод: ").as_html())
    await state.set_state(AddWord.translation)

@user_private_router.message(AddWord.word)
async def add_word_error(message: types.Message):
    await message.answer("Неправильный тип ввода, пожалуйста введите текст!")

@user_private_router.message(AddWord.translation, F.text)
async def add_translation(message: types.Message, state: FSMContext, session: AsyncSession):
    if len(message.text) > 30: 
        await message.answer("Длина слов не может превышать 30 символов! Попробуйте еще раз.")
        return
    if message.text.startswith("/"):
        await message.answer("Команды пока не доступны.")
        return

    await state.update_data(translation=message.text.casefold())
    data = await state.get_data()
    await message.answer(str(data))
    
    try:
        await orm_add_word_translation(session, data)
        await message.answer(
            Bold("Слово успешно добавлено!").as_html(), 
            reply_markup=start_keyboard.as_markup(
                resize_keyboard=True,
                input_field_placeholder="Выберите действие"
            )
        )
    except Exception as e:
        await message.answer(
            Bold(f"Произошла ошибка! {str(e)}").as_html(), 
            reply_markup=start_keyboard.as_markup(
                resize_keyboard=True,
                input_field_placeholder="Выберите действие"
            )
        )
    finally:
        await state.clear()

@user_private_router.message(AddWord.translation)
async def add_translation_error(message: types.Message):
    await message.answer("Неправильный тип ввода, пожалуйста введите текст!")

# delete word
@user_private_router.message(or_f(Command("delete_word"), F.text.lower() == "удалить слово ➖"))
async def delete_word_command(message: types.Message, session: AsyncSession):
    try:
        words_list = await orm_get_all_words_translations(session)
        btns = {
            word_translation.word: f"delete_{word_translation.id}" 
            for word_translation in words_list
        }
        await message.answer(Bold("Какое слово удалить?").as_html(),
                            reply_markup=get_callback_btns(
                                btns=btns,
                                sizes=(1, )
                            ))  
    except Exception as e:
        await message.answer(f"Error {e}")

@user_private_router.callback_query(F.data.startswith("delete_"))
async def delete_word(callback: types.CallbackQuery, session: AsyncSession):
    word_id = int(callback.data.split("_")[-1])

    try:
        await orm_delete_word_translation(session, word_id)
        await callback.answer("Слово удалено!")
        await callback.message.answer(f"Слово удалено!")
    except Exception as e:
        await callback.answer("")
        await callback.message.answer(f"Error {e}")
