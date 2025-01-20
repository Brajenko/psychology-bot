import io
import typing

import matplotlib.pyplot as plt
import sqlalchemy as sa
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import BufferedInputFile, CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.fsm.context import FSMContext
import tgbot.keyboards.inline as inline_kb
from infrastructure.database import models
from tgbot.handlers.llm_handlers import start_helping_dialog

diary_router = Router()


async def add_diary_record(session: AsyncSession, user_id: int, score: int):
    await session.execute(sa.insert(models.DiaryRecord).values(user_id=user_id, score=score))


async def get_diary_records(
    session: AsyncSession, user_id: int
) -> typing.Iterable[models.DiaryRecord]:
    return (
        (
            await session.execute(
                sa.select(models.DiaryRecord).where(models.DiaryRecord.user_id == user_id)
            )
        )
        .scalars()
        .all()
    )


@diary_router.message(F.text, Command("fill_diary"))
async def get_mark(message: Message):
    if message is None:
        return
    await message.answer(
        "Оцените свое эмоционально состояние от 1 до 10:", reply_markup=inline_kb.diary
    )


@diary_router.message(F.text, Command("diary_statistics"))
async def build_graph(message: Message, session: AsyncSession, user: models.User):
    records = await get_diary_records(session, user.id)

    values = [r.score for r in records]
    dates = list(range(1, len(values) + 1))
    dates_labels = [r.created_at.strftime(r"%d/%m/%Y") for r in records]

    plt.figure(figsize=(8, 4))
    plt.plot(list(range(1, len(values) + 1)), values, marker="o", label="Оценка состояния")
    plt.title("Ваш дневник состояния")
    plt.xlabel("Сессии")
    plt.ylabel("Оценка (1-10)")
    plt.grid(True)
    plt.legend()
    plt.xticks(ticks=dates, labels=dates_labels)

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)

    await message.answer_photo(photo=BufferedInputFile(buf.read(), filename="diary.png"))


@diary_router.callback_query(F.data.in_([str(i) for i in range(1, 11)]))
async def handle_diary_callback(
    callback: CallbackQuery, session: AsyncSession, user: models.User, state: FSMContext
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
    if int(selected_value) < 3:
        await start_helping_dialog(
            callback.message,  # type: ignore[arg-type]
            state,
            f"Пользователь поставил низкую оценку ({selected_value}) в своем 'дневнике состояния'",
        )


@diary_router.message(Command("diary_settings"))
async def diary_setup(message: Message):
    await message.answer(
        text="Настройки дневника настроения", reply_markup=inline_kb.diary_settings
    )


@diary_router.callback_query(inline_kb.DiarySettingsCallback.filter())
async def change_diary_settings(
    callback: CallbackQuery,
    callback_data: inline_kb.DiarySettingsCallback,
    user: models.User,
    session: AsyncSession,
):
    await session.execute(
        sa.update(models.User)
        .where(models.User.id == user.id)
        .values(is_diary_on=(callback_data.action == "on"))
    )
    await session.commit()
    await callback.answer("Настройки успешно обновлены!")
