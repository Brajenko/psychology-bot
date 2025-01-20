from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

help_router = Router()

@help_router.message(Command("help"))
async def cmd_help(message: Message):
    help_text = (
        "🔍 <b>Справка по доступным командам:</b>\n\n"
        "📝 <b>Дневник:</b>\n"
        "/fill_diary - Оцените своё эмоциональное состояние по шкале от 1 до 10\n"
        "/diary_statistics - Посмотрите график с вашими оценками состояния\n"
        "/diary_settings - Настройте параметры напоминаний для заполнения дневника\n\n"
        "⚙️ <b>Настройки и информация:</b>\n"
        "/help - Показать это сообщение с описанием команд\n\n"
        "✏️ <b>Тестирование:</b>\n"
        "/start_poll - Пройдите тест для оценки своего состояния\n\n"
    )
    await message.answer(help_text, parse_mode="HTML")
