from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.i18n import i18n_manager


async def get_broadcast_manage_markup(is_subscribed: bool, lang_code: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if is_subscribed:
        builder.add(
            InlineKeyboardButton(
                text=await i18n_manager.get_translation(lang_code, "UNSUBSCRIBE_FROM_BROADCAST_BUTTON_TEXT"),
                callback_data='broadcast_unsubscribe'
            )
        )
    else:
        builder.add(
            InlineKeyboardButton(
                text=await i18n_manager.get_translation(lang_code, "SUBSCRIBE_TO_BROADCAST_BUTTON_TEXT"),
                callback_data='broadcast_subscribe'
            )
        )
    return builder.as_markup()
