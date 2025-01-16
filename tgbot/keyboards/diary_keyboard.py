from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Дневник состояния')]],
                           resize_keyboard=True,
                           input_field_placeholder='Выберите пункт меню...')


diary = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='1', callback_data='1'),
                                               InlineKeyboardButton(text='2', callback_data='2'),
                                               InlineKeyboardButton(text='3', callback_data='3')],
                                               [InlineKeyboardButton(text='4', callback_data='4'),
                                               InlineKeyboardButton(text='5', callback_data='5'),
                                               InlineKeyboardButton(text='6', callback_data='6')],
                                               [InlineKeyboardButton(text='7', callback_data='7'),
                                               InlineKeyboardButton(text='8', callback_data='8'),
                                               InlineKeyboardButton(text='9', callback_data='9')],
                                               [InlineKeyboardButton(text='10', callback_data='10')]])