from typing import List, Dict

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.i18n import i18n_manager


async def get_admin_menu_markup(lang_code: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text=await i18n_manager.get_translation(lang_code, "START_BROADCAST_BUTTON_TEXT"),
                             callback_data="admin_start_broadcast"),
    )
    return builder.as_markup()


def get_broadcast_buttons_markup(buttons_data: List[Dict[str, str]]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for text, url in buttons_data:
        builder.row(InlineKeyboardButton(text=text, url=url))
    return builder.as_markup()


async def get_broadcast_final_markup(lang_code: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text=await i18n_manager.get_translation(lang_code, "SEND_BUTTON_TEXT"),
                             callback_data="admin_send_broadcast_message"),
        InlineKeyboardButton(text=await i18n_manager.get_translation(lang_code, "EDIT_BUTTON_TEXT"),
                             callback_data="admin_edit_broadcast_message"),
    )

    return builder.as_markup()
