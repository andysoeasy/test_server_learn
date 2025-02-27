import os
from dotenv import load_dotenv
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.handlers import router

load_dotenv()

async def init_bot():
    bot = Bot(token=os.getenv('BOT_TOKEN'),
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    
    dp.include_router(router)
    
    await dp.start_polling(bot)