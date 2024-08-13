from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
from bot.i18n import i18n_manager


def get_lang_select_markup():
    lang_buttons = [
        InlineKeyboardButton(
            text=lang_data['NATIVE_LANG_NAME'],
            callback_data=f"lang_{lang_data['LANG_CODE']}")
        for lang_data in i18n_manager.available_languages_data
    ]
    builder = InlineKeyboardBuilder()
    for i in range(0, len(lang_buttons), 3):
        builder.row(*lang_buttons[i:i + 3])
    markup = builder.as_markup()
    return markup
