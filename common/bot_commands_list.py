from aiogram.types import BotCommand

private_commands = [
    BotCommand(command="start", description="Запустить бота"),
    BotCommand(command="menu", description="Меню"),
    BotCommand(command="list", description="Показать мои слова"),
    BotCommand(command="add_word", description="Добавить новое слово"),
    BotCommand(command="delete_word", description="Удалить слово"),
    BotCommand(command="help", description="Помощь"),

]