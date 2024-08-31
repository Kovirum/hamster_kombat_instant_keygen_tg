from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from bot.i18n import i18n_manager
from bot.keyboards import get_admin_menu_markup
from config import ADMIN_ACCESS_IDS
from common.database import db

router = Router()


@router.message(Command('admin'))
async def open_admin_menu(message: Message, state: FSMContext):
    await state.clear()
    lang_code = await db.users_data.get_user_language(message.from_user.id)
    if message.from_user.id not in ADMIN_ACCESS_IDS:
        await message.answer(await i18n_manager.get_translation(lang_code, "ACCESS_DENIED"))
        return
    await message.answer(
        text=await i18n_manager.get_translation(lang_code, "ADMIN_MENU_TITLE"),
        reply_markup=await get_admin_menu_markup(lang_code))


def get_admin_menu_router():
    return router
