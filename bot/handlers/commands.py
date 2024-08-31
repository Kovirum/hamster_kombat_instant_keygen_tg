from aiogram import types, Router, html, F
from aiogram.filters import Command

from bot.i18n import i18n_manager
from bot.keyboards import get_lang_select_markup, delmsg_markup
from bot.keyboards.broadcast_manage_subscribe_kb import get_broadcast_manage_markup
from bot.logic import send_menu_response

from common.database import db

router = Router()


@router.message(Command('start'))
async def send_welcome(message: types.Message):
    await message.answer("Choose a language/Выберите язык", reply_markup=get_lang_select_markup())


@router.message(Command("menu"))
async def open_menu(message: types.Message):
    await send_menu_response(message, message.from_user.id)


@router.message(Command('language'))
async def language_choice(message: types.Message):
    await message.answer("Choose a language/Выберите язык", reply_markup=get_lang_select_markup())


@router.message(F.text.lower() == '/myid')
async def my_id(message: types.Message):
    await message.answer(html.code(message.from_user.id), reply_markup=delmsg_markup)


@router.message(Command('broadcast'))
async def broadcast(message: types.Message):
    user_doc = await db.users_data.init_user(message.from_user.id)
    broadcast_subscribe_status = user_doc.get('broadcast') or False
    lang_code = await db.users_data.get_user_language(message.from_user.id)
    markup = await get_broadcast_manage_markup(broadcast_subscribe_status, lang_code)

    status_text = await i18n_manager.get_translation(
        lang_code,
        "SUBSCRIPTION_ACTIVE" if broadcast_subscribe_status else "SUBSCRIPTION_INACTIVE"
    )

    await message.answer(
        text=(await i18n_manager.get_translation(lang_code, "CURRENT_BROADCAST_SUBSCRIPTION_STATUS")).format(
            status=status_text),
        reply_markup=markup
    )



def register_commands_handler(dp):
    dp.include_router(router)
