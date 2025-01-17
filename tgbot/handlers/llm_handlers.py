from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from tgbot.gigachat.llm_init import get_response
from infrastructure.database.models import User
from tgbot.misc.states import LLM

gigachat_router = Router()


@gigachat_router.message(F.text)
async def message_to_llm(message: types.Message, user: User):
    await message.answer(await get_response(user, user_input=message.text))


@gigachat_router.message(F.text, StateFilter(LLM.helping))
async def llm_helping(message: types.Message, state: FSMContext, user: User):
    await state.get_value("problem") # TODO: проблема пользователя, можно засунуть в ллм
    await message.answer(await get_response(user, user_input=message.text))


async def start_helping_dialog(message: types.Message, state: FSMContext):
    await message.answer(
        "Результаты твоего теста/дневника выглядят не очень( Не хочешь обсудить свои проблемы со мной? Это может помочь"
    )
    await state.set_state(LLM.helping)
    await state.set_data(
        {
            "problem": "сюда можно указать какой конкретно тест пользователь плохо прошел но в целом это не обязательно"
        }
    )
