import aiogram
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.i18n import i18n_manager
from config import SUBSCRIBE_REQUIRED_CHANNEL_LIST


async def get_subscription_check_markup(lang_code: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for channel_data in SUBSCRIBE_REQUIRED_CHANNEL_LIST:
        builder.row(
            InlineKeyboardButton(
                text=channel_data['name'],
                url=channel_data['invite_link'],
            )
        )
    builder.row(
        InlineKeyboardButton(
            text=await i18n_manager.get_translation(lang_code, "CHECK_SUBSCRIPTION"),
            callback_data='check_subscription')
    )

    markup = builder.as_markup()
    return markup
