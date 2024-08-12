from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from config import SUBSCRIBE_REQUIRED_CHANNEL_INVITE_LINK

builder = InlineKeyboardBuilder()
builder.add(
    InlineKeyboardButton(text="Subscribe to the channel", url=SUBSCRIBE_REQUIRED_CHANNEL_INVITE_LINK),
    InlineKeyboardButton(text="Check your subscription", callback_data='check_subscription')
)

subcheck_markup = builder.as_markup()