from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

import tgbot.keyboards.diary_keyboard as kb
from tgbot.misc.states import MarkChoose


diary_router = Router()


@diary_router.message(F.text == "Дневник состояния")
async def get_mark(message: Message):
    await message.answer("Оцените свое эмоционально состояние от 1 до 10:", reply_markup=kb.diary)

@diary_router.callback_query(F.data.in_([str(i) for i in range(1, 11)]))
async def handle_diary_callback(callback: CallbackQuery):
    selected_value = callback.data
    await callback.message.answer(f"Вы оценили ваше текущее эмоциональное состояние на {selected_value}/10.")
    await callback.answer()
