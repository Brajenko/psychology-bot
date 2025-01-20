from aiogram import F, Router
from aiogram.types import Message

wrong_command_router = Router()

@wrong_command_router.message(F.text.startswith("/") & ~F.text.in_({"start", "help", "fill_diary", "diary_statistics", "diary_settings", "start_poll"}))
async def catch_wrong_command(message: Message):
    await message.answer("Такой команды нет. Список доступных команд можно посмотреть с помощью команды /help.")
