import asyncio
from config import KEYGEN_ACTIVE

from app.bot import startup_bot
from tools.key_generator import start_generating_keys


async def start():
    if KEYGEN_ACTIVE:
        start_generating_keys()
    await startup_bot()


if __name__ == "__main__":
    asyncio.run(start())
