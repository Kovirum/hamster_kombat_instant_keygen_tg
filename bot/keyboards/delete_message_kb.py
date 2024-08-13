from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

builder = InlineKeyboardBuilder()
delmsg_button = InlineKeyboardButton(text="🗑️", callback_data='delete_message')
builder.row(delmsg_button)

delmsg_markup = builder.as_markup()
