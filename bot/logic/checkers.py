import aiogram
import logging
from config import SUBSCRIBE_REQUIRED_CHANNEL_LIST


async def check_user_channel_subscription(bot: aiogram.Bot, user_id: int) -> bool:
    if SUBSCRIBE_REQUIRED_CHANNEL_LIST is None:
        return True
    success = True
    for channel_data in SUBSCRIBE_REQUIRED_CHANNEL_LIST:
        try:
            chat_member = await bot.get_chat_member(channel_data['id'], user_id)
            if chat_member.status in ('member', 'administrator', 'creator'):
                pass
            else:
                success = False
                break
        except Exception as e:
            logging.error(e)
            success = False
            break
    return success
