from aiogram import types, Router, F
from aiogram.utils.markdown import hcode
from tgbot.gigachat.llm_init import get_response
from infrastructure.database.models import User

gigachat_router = Router()

@gigachat_router.message(F.text)
async def message_to_llm(message: types.Message, user: User):
    await message.answer(await get_response(user, user_input=message.text))
