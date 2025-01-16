from aiogram import types, Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hcode
from tgbot.gigachat.llm_init import get_response
from infrastructure.database.models import User

gigachat_router = Router()

@gigachat_router.message(F.text, StateFilter(None))
async def bot_echo(message: types.Message, user: User):
    await message.answer(await get_response(user_id=user.id, user_input=message.text))

@gigachat_router.message(F.text)
async def bot_echo_all(message: types.Message, state: FSMContext):
    state_name = await state.get_state()
    text = [
        f"Эхо в состоянии {hcode(state_name)}",
        "Содержание сообщения:",
        hcode(message.text),
    ]
    await message.answer("\n".join(text))
