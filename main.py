import asyncio
from config import STARTUP_METHOD, StartupMethods

import logging
logging.basicConfig(level=logging.INFO)


async def start():
    if STARTUP_METHOD in (StartupMethods.OnlyKeygen, StartupMethods.KeygenAndBot):
        from keygen.key_generator import start_generating_keys
        start_generating_keys()
    if STARTUP_METHOD in (StartupMethods.OnlyBot, StartupMethods.KeygenAndBot):
        from bot.startup import startup_bot
        await startup_bot()


if __name__ == "__main__":
    asyncio.run(start())
