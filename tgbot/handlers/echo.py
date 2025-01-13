from aiogram import types, Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hcode

from infrastructure.database.models import User

echo_router = Router()


@echo_router.message(F.text, StateFilter(None))
async def bot_echo(message: types.Message, user: User):
    await message.answer(f"{user.call_name} said:\n{message.text}")


@echo_router.message(F.text)
async def bot_echo_all(message: types.Message, state: FSMContext):
    state_name = await state.get_state()
    text = [
        f"Эхо в состоянии {hcode(state_name)}",
        "Содержание сообщения:",
        hcode(message.text),
    ]
    await message.answer("\n".join(text))
