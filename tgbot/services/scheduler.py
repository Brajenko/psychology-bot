import datetime as dt
import logging
import typing

import sqlalchemy as sa
from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

import tgbot.keyboards.inline as inline_kb
from infrastructure.database import models
from infrastructure.database.setup import create_engine, create_session_pool
from tgbot.config import load_config

from .broadcaster import send_message

dr1 = aliased(models.DiaryRecord)
dr2 = aliased(models.DiaryRecord)

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


async def get_users_to_send_diary(session: AsyncSession) -> typing.Iterable[int]:
    all_user_ids = (await session.execute(sa.select(models.User.id))).scalars().all()
    user_ids: list[int] = []
    for user_id in all_user_ids:
        last_diary_ts = (
            await session.execute(
                sa.select(models.DiaryRecord.created_at)
                .where(models.DiaryRecord.user_id == user_id)
                .order_by(models.DiaryRecord.created_at.desc())
                .limit(1)
            )
        ).scalar_one_or_none()
        if last_diary_ts is None or last_diary_ts < dt.datetime.now() - dt.timedelta(
            days=1
        ):
            user_ids.append(user_id)
    return user_ids


async def update_user_sent_diary(session: AsyncSession, user_id: int):
    await session.execute(
        sa.update(models.User)
        .where(models.User.id == user_id)
        .values(last_diary_sent=sa.func.now())
    )
    await session.commit()


async def send_periodic_message(bot: Bot):
    async with create_session_pool(create_engine(load_config(".env").db))() as session:  # type: ignore
        user_ids = await get_users_to_send_diary(session)
        for user_id in user_ids:
            if await send_message(
                bot,
                user_id,
                text="Оцените свое эмоциональное состояние от 1 до 10:",
                reply_markup=inline_kb.diary,
            ):
                await update_user_sent_diary(session, user_id)
