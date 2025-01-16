from aiogram import types, Router, F
from aiogram.filters import StateFilter
# from aiogram.fsm.context import FSMContext
from gigachat.llm_init import get_response

from infrastructure.database.models import User

gigachat_router = Router()

@gigachat_router.message(F.text, StateFilter(None))
async def bot_echo(message: types.Message, user: User):
    await message.answer(get_response(user_id=user.id, user_input=message))
