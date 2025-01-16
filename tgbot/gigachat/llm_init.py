from langchain_gigachat.chat_models import GigaChat
from environs import Env
from langchain.chains import ConversationChain
from langchain.memory import ConversationSummaryBufferMemory
from .prompts import *
import asyncio

# Асинхронная блокировка
lock = asyncio.Lock()

def get_gigachat(path: str | None = None):
    env = Env()
    env.read_env(path)
    return GigaChat(
        credentials=env.str("GIGACHAT_API_AUTH_KEY"),
        model='GigaChat:latest',
        verify_ssl_certs=False,
    )

# Контейнер памяти для пользователей
user_contexts = {}

async def get_user_context(user_id):
    """Получить контекст пользователя или создать новый (асинхронно)"""
    async with lock:  # Асинхронная блокировка
        if user_id not in user_contexts:
            gigachat = get_gigachat(".env")
            user_contexts[user_id] = ConversationChain(
                llm=gigachat,
                verbose=True,
                prompt=BASIC_PROMPT,
                memory=ConversationSummaryBufferMemory(llm=gigachat, memory_key="summary")
            )
    return user_contexts[user_id]

async def get_response(user_id, user_input):
    """Получение ответа от LLM для конкретного пользователя"""
    context = await get_user_context(user_id)  # Асинхронный вызов
    response = await asyncio.to_thread(context.predict, input=user_input)  # Запуск вычисления в отдельном потоке
    return response  # Возвращаем результат