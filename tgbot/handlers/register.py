from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.fsm.state import State
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.models import User
from tgbot.misc.states import Registration

register_router = Router()


@register_router.message(CommandStart())
async def command_start(message: Message, user: User, state: FSMContext) -> None:
    s: State | None = Registration.name
    if user.call_name is not None:
        s = Registration.age
        if user.age is not None:
            s = None
    await state.set_state(s)
    if s == Registration.name:
        await message.answer("Привет! Подскажи, как лучше к тебе обращаться?")
    else:
        await message.answer("Ты уже зарегистрирован! Попробуй /help")


@register_router.message(Registration.name)
async def process_name(message: Message, state: FSMContext, user: User, session: AsyncSession):
    if message.text:
        if len(message.text) > 128:
            await message.answer("Имя слишком длинное! Попробуй еще раз.")
            return
        user.call_name = message.text
        await session.commit()
        await message.answer(f"Приятно познакомиться, {message.text}! Сколько тебе лет?")
        await state.set_state(Registration.age)
    else:
        await message.answer("Пожалуйста, введи свое имя!")


@register_router.message(Registration.age)
async def process_age(message: Message, state: FSMContext, user: User, session: AsyncSession):
    if message.text is not None and message.text.isdigit():
        if int(message.text) < 0:
            await message.answer("Возраст не может быть отрицательным! Попробуй еще раз.")
            return
        user.age = int(message.text)
        await session.commit()
        await state.clear()
        await message.answer(
            "Ты зарегистрирован! Теперь можешь пользоваться всеми функциями бота. Подсказка: попробуй /help"
        )
    else:
        await message.answer("Не понимаю( Пожалуйста, введи свой возраст цифрами!")
