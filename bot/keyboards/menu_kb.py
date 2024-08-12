from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from config import SUBSCRIBE_REQUIRED_CHANNEL_INVITE_LINK, GamePromoTypes
from .delete_message_kb import delmsg_button

builder = InlineKeyboardBuilder()
game_buttons = [InlineKeyboardButton(text=game.value, callback_data=game.value) for game in GamePromoTypes]
for i in range(0, len(game_buttons), 2):
    builder.row(*game_buttons[i:i + 2])

builder.row(InlineKeyboardButton(text="🔁", callback_data='update_menu'), delmsg_button)
builder.row(InlineKeyboardButton(text="History", callback_data="history_menu"))
builder.row(InlineKeyboardButton(text="Powered by Project PDoSI", url=SUBSCRIBE_REQUIRED_CHANNEL_INVITE_LINK))

menu_markup = builder.as_markup()
