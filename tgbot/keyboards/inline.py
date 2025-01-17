import typing

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.filters.callback_data import CallbackData


diary = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="1", callback_data="1"),
            InlineKeyboardButton(text="2", callback_data="2"),
            InlineKeyboardButton(text="3", callback_data="3"),
        ],
        [
            InlineKeyboardButton(text="4", callback_data="4"),
            InlineKeyboardButton(text="5", callback_data="5"),
            InlineKeyboardButton(text="6", callback_data="6"),
        ],
        [
            InlineKeyboardButton(text="7", callback_data="7"),
            InlineKeyboardButton(text="8", callback_data="8"),
            InlineKeyboardButton(text="9", callback_data="9"),
        ],
        [InlineKeyboardButton(text="10", callback_data="10")],
    ]
)


class DiarySettingsCallback(CallbackData, prefix="diary-settings"):
    action: typing.Literal["off", "on"]


diary_settings = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Включить", callback_data=DiarySettingsCallback(action="on").pack()
            )
        ],
        [
            InlineKeyboardButton(
                text="Выключить", callback_data=DiarySettingsCallback(action="off").pack()
            )
        ],
    ]
)
