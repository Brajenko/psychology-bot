from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.database import models
import tgbot.keyboards.diary_keyboard as kb
import sqlalchemy as sa

diary_router = Router()


async def add_diary_record(session: AsyncSession, user_id: int, score: int):
    await session.execute(
        sa.insert(models.DiaryRecord).values(user_id=user_id, score=score)
    )


@diary_router.message(F.text == "Дневник состояния")
async def get_mark(message: Message):
    if message is None:
        return
    await message.answer(
        "Оцените свое эмоционально состояние от 1 до 10:", reply_markup=kb.diary
    )


@diary_router.callback_query(F.data.in_([str(i) for i in range(1, 11)]))
async def handle_diary_callback(
    callback: CallbackQuery, session: AsyncSession, user: models.User
):
    selected_value = callback.data
    if callback.message is None or selected_value is None:
        return
    await add_diary_record(session, user.id, int(selected_value))
    await callback.message.answer(
        f"Вы оценили ваше текущее эмоциональное состояние на {selected_value}/10."
    )
    await callback.answer()
    await session.commit()
