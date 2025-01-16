from langchain_gigachat.chat_models import GigaChat
from environs import Env
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from prompts import *

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

def get_user_context(user_id):
    """Получить контекст пользователя или создать новый"""
    if user_id not in user_contexts:
        gigachat = get_gigachat(".env")
        user_contexts[user_id] = ConversationChain(
            llm=gigachat,
            verbose=True,
            prompt=BASIC_PSYCHOLOGY_PROMPT,
            memory=ConversationBufferMemory(llm=gigachat)
        )
    return user_contexts[user_id]

async def get_response(user_id, user_input):
    """Получение ответа от LLM для конкретного пользователя"""
    context = get_user_context(user_id)
    context.predict(input=user_input)
    return context.memory.chat_memory.messages[-1].content