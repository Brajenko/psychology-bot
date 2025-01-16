import os
import matplotlib.pyplot as plt
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import CommandStart

import app.keyboards as kb
from app.scheduler import start_scheduler, stop_scheduler

router = Router()

# Хранилище пользователей
users = set()

# Хранилище оценок
user_diary = {}

@router.message(CommandStart())
async def cmd_start(message: Message):
    users.add(message.from_user.id)
    await message.answer("Привет!", reply_markup=kb.main)


@router.message(F.text == "Дневник состояния")
async def get_mark(message: Message):
    await message.answer("Оцените свое эмоционально состояние от 1 до 10:", reply_markup=kb.diary)


@router.callback_query(F.data.in_([str(i) for i in range(1, 11)]))
async def handle_diary_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    selected_value = int(callback.data)  # Получаем оценку

    # Сохраняем оценку в словаре user_diary
    if user_id not in user_diary:
        user_diary[user_id] = []  # Если пользователь новый — создаем список
    user_diary[user_id].append(selected_value)  # Добавляем оценку в список

    # Ответ пользователю
    await callback.message.answer(f"Вы оценили ваше текущее эмоциональное состояние на {selected_value}/10.")
    await callback.answer()


@router.message(F.text == "Построить график")
async def build_graph(message: Message):
    user_id = message.from_user.id

    # Проверка: есть ли данные для текущего пользователя
    if user_id not in user_diary or not user_diary[user_id]:
        await message.answer("У вас пока нет данных для построения графика.")
        return

    # Создаем директорию, если она не существует
    graphics_dir = "graphics"
    if not os.path.exists(graphics_dir):
        os.makedirs(graphics_dir)  # Создаем директорию

    # Построение графика

    dates = list(range(1, len(user_diary[user_id]) + 1))  # Эмулируем даты как 1, 2, 3...
    values = user_diary[user_id]

    plt.figure(figsize=(8, 4))
    plt.plot(dates, values, marker='o', label="Оценка состояния")
    plt.title("Ваш дневник состояния")
    plt.xlabel("Сессии")
    plt.ylabel("Оценка (1-10)")
    plt.grid(True)
    plt.legend()
    plt.xticks(ticks=dates)

    # Сохраняем график в директории
    plt.savefig(os.path.join(graphics_dir, "graphic.png"))

    file_path = os.path.join(graphics_dir, "graphic.png")

    await message.answer_photo(photo=FSInputFile(path=file_path))

@router.message(F.text == "Управление рассылкой")
async def manage_scheduler(message: Message):
    await message.answer("Вы можете включить или отключить рассылку:", reply_markup=kb.scheduler_control)


@router.callback_query(F.data == "start_scheduler")
async def start_scheduler_callback(callback: CallbackQuery):
    bot = callback.bot  # Получаем объект bot из callback
    start_scheduler(bot, users)  # Передаём bot и users
    await callback.answer("Рассылка включена.")


@router.callback_query(F.data == "stop_scheduler")
async def stop_scheduler_callback(callback: CallbackQuery):
    stop_scheduler()
    await callback.answer("Рассылка остановлена.")