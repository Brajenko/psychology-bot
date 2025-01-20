import typing

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import Scene, SceneRegistry, ScenesManager, on
from aiogram.types import Message, ReplyKeyboardRemove
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from infrastructure.database.models import Poll, Question, Result
from tgbot.keyboards.reply import (
    generate_keyboard_for_poll_choosing,
    generate_keyboard_for_question,
)
from tgbot.handlers.llm_handlers import start_helping_dialog
from tgbot.misc.states import PollChoose


async def get_current_question(session: AsyncSession, poll_id: int, step: int) -> Question | None:
    return (
        await session.execute(
            select(Question)
            .filter(Question.poll_id == poll_id)
            .limit(1)
            .offset(step)
            .options(selectinload(Question.variants))
        )
    ).scalar_one_or_none()


async def get_polls(session: AsyncSession) -> typing.Iterable[Poll]:
    p = (await session.execute(select(Poll))).scalars().all()
    return p


async def get_poll(session: AsyncSession, poll_id: int) -> Poll:
    return (await session.execute(select(Poll).filter(Poll.id == poll_id))).scalar_one()


async def get_poll_by_name(session: AsyncSession, poll_name: str) -> Poll | None:
    return (await session.execute(select(Poll).filter(Poll.name == poll_name))).scalar_one_or_none()


async def get_results(session: AsyncSession, poll_id: int, score: int) -> Result:
    return (
        await session.execute(
            select(Result)
            .filter(Result.poll_id == poll_id)
            .filter(Result.min_points <= score)
            .filter(Result.max_points >= score)
        )
    ).scalar_one()


class PollScene(Scene, state="poll"):
    @on.message.enter()
    async def on_enter(
        self,
        message: Message,
        state: FSMContext,
        session: AsyncSession,
        poll_id: int,
        step: int = 0,
        score: int = 0,
    ) -> typing.Any:
        await state.update_data(step=step, poll_id=poll_id, score=score)

        p = await get_poll(session, poll_id)
        if step == 0 and p.intro:
            await message.answer(p.intro)

        q = await get_current_question(session, poll_id, step)
        if q is None:
            return await self.wizard.exit(session=session, state=state)

        return await message.answer(
            text=q.content,
            reply_markup=generate_keyboard_for_question(q),
        )

    @on.message.exit()
    async def on_exit(
        self,
        message: Message,
        session: AsyncSession,
        state: FSMContext,
        silent: bool = False,
    ) -> None:
        if silent:
            return await state.clear()
        data = await state.get_data()
        score: int = data["score"]
        res = await get_results(session, data["poll_id"], score)
        await message.answer("Ваш результат: " + res.content, reply_markup=ReplyKeyboardRemove())
        poll = await get_poll(session, data["poll_id"])
        await state.clear()
        if res.is_critical:
            await start_helping_dialog(
                message,
                state,
                f"Пользователь прошел тест {poll.name} и получил плохой результат {res.content}",
            )

    @on.message()
    async def answer(self, message: Message, state: FSMContext, session: AsyncSession) -> None:
        data = await state.get_data()
        step: int = data["step"]
        score: int = data["score"]
        q = await get_current_question(session, data["poll_id"], step)
        if q is None:
            return await self.wizard.exit(session=session, state=state)
        try:
            v = next((v for v in q.variants if v.content == message.text))
        except StopIteration:
            await message.answer("Нужно выбрать один из вариантов ответа")
            return

        score += v.points
        await self.wizard.retake(
            step=step + 1, poll_id=data["poll_id"], score=score, session=session
        )


poll_router = Router(name=__name__)


@poll_router.message(Command("start_poll"))
async def command_start(
    message: Message, scenes: ScenesManager, state: FSMContext, session: AsyncSession
) -> None:
    await message.answer(
        "Привет! Выбери один из тестов для прохождения",
        reply_markup=generate_keyboard_for_poll_choosing(await get_polls(session)),
    )
    await state.set_state(PollChoose.choose)


@poll_router.message(PollChoose.choose)
async def poll_choose(
    message: Message,
    state: FSMContext,
    scenes: ScenesManager,
    session: AsyncSession,
) -> None:
    poll = await get_poll_by_name(session, message.text or "")
    if not message.text or not poll:
        await message.answer("Выбери тест из списка")
        return
    await scenes.enter(PollScene, poll_id=poll.id, session=session)
    await state.set_state("poll")


scene_registry = SceneRegistry(poll_router)
scene_registry.add(PollScene)
