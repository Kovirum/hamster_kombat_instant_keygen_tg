import os

import aiogram
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from .handlers import register_handlers
from .i18n import i18n_manager
from dotenv import load_dotenv


load_dotenv()

bot = Bot(
    token=os.getenv('BOT_TOKEN'),
    default=aiogram.client.default.DefaultBotProperties(
        parse_mode=ParseMode.HTML
    ))
dp = Dispatcher(storage=MemoryStorage())


async def startup_bot():
    await i18n_manager.init()
    register_handlers(dp)
    await dp.start_polling(bot, skip_updates=True)
