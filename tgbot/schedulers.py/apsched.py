from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot
import tgbot.keyboards.diary_keyboard as kb

# Инициализация планировщика
scheduler = AsyncIOScheduler()

async def send_periodic_message(bot: Bot, users: set):
    for user_id in users:
        try:
            await bot.send_message(
                chat_id=user_id,
                text="Оцените свое эмоциональное состояние от 1 до 10:",
                reply_markup=kb.diary
            )
        except Exception as e:
            print(f"Ошибка при отправке сообщения пользователю {user_id}: {e}")

def start_scheduler(bot: Bot, users: set):
    scheduler.add_job(send_periodic_message, "interval", seconds=15, args=[bot, users])
    scheduler.start()

def stop_scheduler():
    scheduler.shutdown()
