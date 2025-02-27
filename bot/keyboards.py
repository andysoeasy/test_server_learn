from aiogram.types import (
    ReplyKeyboardMarkup, 
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    WebAppInfo
)

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Мои заказы')],
        [KeyboardButton(text='О компании')]
    ],
    resize_keyboard=True,
    input_field_placeholder='Выберите пункт меню...'
)

menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Открыть магазин', web_app=WebAppInfo(url=f'https://ya.ru/'))],
        [InlineKeyboardButton(text='Дополнительно', callback_data=f'additionaly')]
    ]
)








