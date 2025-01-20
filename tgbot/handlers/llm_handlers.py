from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from tgbot.gigachat.llm_init import get_response
from infrastructure.database.models import User

gigachat_router = Router()


async def start_helping_dialog(message: types.Message, state: FSMContext, problem: str):
    await message.answer(
        "Результаты твоего теста/дневника выглядят не очень( Не хочешь обсудить свои проблемы со мной? Это может помочь"
    )
    await state.set_data({"problem": problem})


@gigachat_router.message(F.text)
async def message_to_llm(message: types.Message, user: User, state: FSMContext):
    problem = await state.get_value("problem")
    await message.answer(await get_response(user, user_input={message.text}, problem=problem))
    if problem is not None:
        await state.clear()
