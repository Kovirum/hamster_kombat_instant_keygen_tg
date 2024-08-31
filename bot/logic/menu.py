from aiogram import types
from aiogram.utils.formatting import as_list, as_marked_section, Bold, as_key_value

from bot.keyboards import get_menu_markup, get_subscription_check_markup
from bot.i18n import i18n_manager
from bot.logic.checkers import check_user_channel_subscription
from common.database import db
from config import GamePromoTypes


async def send_menu_response(message: types.Message, user_id: int):
    lang_code = await db.users_data.get_user_language(user_id)
    access = await check_user_channel_subscription(message.bot, user_id)
    if not access:
        await message.answer(
            text=await i18n_manager.get_translation(lang_code, "MUST_SUBSCRIBE_REQUIRED_CHANNEL"),
            reply_markup=await get_subscription_check_markup(lang_code))
        return

    response = as_list(
        as_marked_section(
            Bold(await i18n_manager.get_translation(lang_code, "TOTAL_KEYS")),
            *[as_key_value(game.value, await db.keys_pool.count_key_pool(game)) for game in GamePromoTypes]
        ),
        as_marked_section(
            Bold(await i18n_manager.get_translation(lang_code, "AVAILABLE_DAILY_KEYS")),
            *[
                as_key_value(
                    game.value,
                    '/'.join(map(str, await db.users_data.get_pool_limit(game, user_id)))
                )
                for game in GamePromoTypes
            ]
        ),
        sep='\n\n'
    )
    await message.answer(response.as_html(), reply_markup=await get_menu_markup(lang_code))
