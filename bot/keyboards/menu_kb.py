from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import PROJECT_PDOSI_INVITE_URL, GamePromoTypes
from .delete_message_kb import delmsg_button

from bot.i18n import i18n_manager


async def get_menu_markup(lang_code: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    game_buttons = [InlineKeyboardButton(text=game.value, callback_data=game.value) for game in GamePromoTypes]
    for i in range(0, len(game_buttons), 2):
        builder.row(*game_buttons[i:i + 2])

    builder.row(InlineKeyboardButton(text="🔁", callback_data='update_menu'), delmsg_button)
    builder.row(InlineKeyboardButton(
        text=await i18n_manager.get_translation(lang_code, "HISTORY_BUTTON_LABEL"),
        callback_data="history_menu"))
    # YOU MUST KEEP THIS LINK OR OTHER MENTION OF AUTHORSHIP IN ORDER TO PRESERVE THE LICENSE
    builder.row(InlineKeyboardButton(
        text=await i18n_manager.get_translation(lang_code, "POWERED_BY_LABEL"),
        url=PROJECT_PDOSI_INVITE_URL))

    menu_markup = builder.as_markup()
    return menu_markup
