import asyncio
from config import STARTUP_METHOD, StartupMethods

from app.bot import startup_bot
from tools.key_generator import start_generating_keys

import logging
logging.basicConfig(level=logging.INFO)


async def start():
    if STARTUP_METHOD in (StartupMethods.OnlyKeygen, StartupMethods.KeygenAndBot):
        start_generating_keys()
    if STARTUP_METHOD in (StartupMethods.OnlyBot, StartupMethods.KeygenAndBot):
        await startup_bot()
    print("Gg")


if __name__ == "__main__":
    asyncio.run(start())
