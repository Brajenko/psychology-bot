import asyncio

from environs import Env
from langchain.chains import ConversationChain
from langchain.memory import ConversationSummaryBufferMemory
from langchain_core.messages import SystemMessage
from langchain_gigachat.chat_models import GigaChat
from langchain.prompts import PromptTemplate

from infrastructure.database.models import User

from .prompts import BASIC_PROMPT_TEMPLATE, PROBLEM_PROMPT

# Асинхронная блокировка
lock = asyncio.Lock()


def get_gigachat(path: str | None = None):
    env = Env()
    env.read_env(path)
    return GigaChat(
        credentials=env.str("GIGACHAT_API_AUTH_KEY"),
        model="GigaChat:latest",
        verify_ssl_certs=False,
    )


# Контейнер памяти для пользователей
user_contexts = {}


async def get_user_context(user: User):
    """Получить контекст пользователя или создать новый (асинхронно)"""
    async with lock:  # Асинхронная блокировка
        if user.id not in user_contexts:
            gigachat = get_gigachat(".env")
            user_contexts[user.id] = ConversationChain(
                llm=gigachat,
                verbose=True,
                prompt=PromptTemplate(
                    template=BASIC_PROMPT_TEMPLATE.format(username=user.call_name, age=user.age),
                    input_variables=["history", "input"]
                ),
                memory=ConversationSummaryBufferMemory(llm=gigachat, memory_key="summary"),
            )
    return user_contexts[user.id]


async def get_response(user: User, user_input: set[str], problem: str | None = None):
    """Получение ответа от LLM для конкретного пользователя"""
    context = await get_user_context(user)  # Асинхронный вызов
    if problem is not None:
        context.memory.chat_memory.add_ai_message(
            "Результаты твоего теста/дневника выглядят не очень( Не хочешь обсудить свои проблемы со мной? Это может помочь"
        )
        context.memory.chat_memory.add_message(SystemMessage(PROBLEM_PROMPT + problem))
    response = await asyncio.to_thread(
        context.predict, input=user_input
    )  # Запуск вычисления в отдельном потоке
    return response  # Возвращаем результат
