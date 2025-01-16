import typing
from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from infrastructure.database.models import Question, Poll


def generate_keyboard_for_question(q: Question) -> ReplyKeyboardMarkup:
    rkb = ReplyKeyboardBuilder()
    for v in q.variants:
        rkb.row(KeyboardButton(text=v.content))
    return rkb.as_markup(resize_keyboard=True)


def generate_keyboard_for_poll_choosing(polls: typing.Iterable[Poll]) -> ReplyKeyboardMarkup:
    rkb = ReplyKeyboardBuilder()
    for p in polls:
        rkb.add(KeyboardButton(text=p.name))
    return rkb.as_markup(resize_keyboard=True, one_time_keyboard=True)
