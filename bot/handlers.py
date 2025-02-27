from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

import database.requests as rq


import bot.keyboards as kb

router = Router()

start_message = '''
Привет!
Добро пожаловать в бот доставки вкусной еды SUPERFOOD.
Чтобы приступить к заказу нажмите на кнопку <b>"Открыть магазин"</b>.
Для получения дополнительной информации нажмите на кнопку
<b>"Дополнительно"</b>
'''

help_message = '''
Чтобы перейти к выбору блюд нажмите кнопку ниже.
'''

about_message = '''
Здесь будет информация о компании
'''


@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.add_user(message.from_user.id)
    await message.answer(start_message, reply_markup=kb.menu)
    

@router.message(F.text == 'Мои заказы')
async def cmd_last_orders(message: Message):
    user = await rq.add_user(message.from_user.id)
    orders = await rq.get_orders(user.id)
    
    if orders:
        await message.answer('Ваши заказы:')
        for order in orders:
            formatted_message = (
                f'<b>Дата заказа: </b> {order["date_create_order"]}\n'
                f'<b>Позиции: </b> {order["items"]}\n'
                f'<b>Общая стоимость: </b> {order["total_cost"]}\n'
            )
            await message.answer(formatted_message)
    else:
        await message.answer('У вас еще нет заказов')
        

@router.message(F.text == 'О компании')
async def cmd_about(message: Message):
    await message.answer(about_message)


@router.callback_query(F.data == 'additionaly')
async def view_additionaly_info(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.answer(
        'Для просмотра дополнительной информации воспользуйтесь <b>меню</b>',
        reply_markup=kb.main_keyboard
    )