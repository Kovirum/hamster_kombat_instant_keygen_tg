import aiogram
import logging
from config import SUBSCRIBE_REQUIRED_CHANNEL_ID


async def check_user_channel_subscription(bot: aiogram.Bot, user_id: int) -> bool:
    try:
        chat_member = await bot.get_chat_member(SUBSCRIBE_REQUIRED_CHANNEL_ID, user_id)
        if chat_member.status in ('member', 'administrator', 'creator'):
            return True
        else:
            return False
    except Exception as e:
        logging.error(e)
        return False
