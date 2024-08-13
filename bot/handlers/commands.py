from aiogram import types, Router, html, F
from aiogram.filters import Command

from bot.keyboards import get_lang_select_markup, delmsg_markup
from bot.logic import send_menu_reponse

router = Router()


@router.message(Command('start'))
async def send_welcome(message: types.Message):
    await message.answer("Choose a language/Выберите язык", reply_markup=get_lang_select_markup())


@router.message(Command("menu"))
async def open_menu(message: types.Message):
    await send_menu_reponse(message, message.from_user.id)


@router.message(Command('language'))
async def language_choice(message: types.Message):
    await message.answer("Choose a language/Выберите язык", reply_markup=get_lang_select_markup())


@router.message(F.text.lower() == '/myid')
async def my_id(message: types.Message):
    await message.answer(html.code(message.from_user.id), reply_markup=delmsg_markup)


def register_start_handler(dp):
    dp.include_router(router)
