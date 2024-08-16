import asyncio
from config import STARTUP_METHOD, StartupMethods

import logging
logging.basicConfig(level=logging.INFO)


async def start():
    if STARTUP_METHOD in (StartupMethods.OnlyKeygen, StartupMethods.KeygenAndBot):
        from keygen.key_generator import keygen_startup
        await asyncio.create_task(keygen_startup())
    if STARTUP_METHOD in (StartupMethods.OnlyBot, StartupMethods.KeygenAndBot):
        from bot.startup import startup_bot
        await startup_bot()


if __name__ == "__main__":
    asyncio.run(start())
