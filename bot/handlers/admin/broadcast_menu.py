from aiogram import F, Router
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.i18n import i18n_manager
from bot.logic.broadcast import get_broadcast_response, start_broadcast
from bot.states import BroadcastStates
from common.database import db
from config import ADMIN_ACCESS_IDS

router = Router()


@router.callback_query(StateFilter(None), F.data.in_(['admin_start_broadcast', 'admin_edit_broadcast_message']))
async def admin_start_broadcast(callback: CallbackQuery, state: FSMContext):
    lang_code = await db.users_data.get_user_language(callback.from_user.id)
    if (await state.get_data()).get('text'):
        await callback.message.answer(await i18n_manager.get_translation(lang_code, "ENTER_BROADCAST_TEXT_SKIP"))
    else:
        await callback.message.answer(await i18n_manager.get_translation(lang_code, "ENTER_BROADCAST_TEXT"))
    await state.set_state(BroadcastStates.add_broadcast_text)


@router.callback_query(StateFilter(None), F.data == 'admin_send_broadcast_message')
async def admin_send_broadcast_message(callback: CallbackQuery, state: FSMContext):
    lang_code = await db.users_data.get_user_language(callback.from_user.id)
    if callback.from_user.id not in ADMIN_ACCESS_IDS:
        await callback.message.answer(await i18n_manager.get_translation(lang_code, "ACCESS_DENIED"))
        return
    await start_broadcast(callback.message, state)


@router.message(Command('skip'))
async def skip_state(message: Message, state: FSMContext):
    lang_code = await db.users_data.get_user_language(message.from_user.id)
    current_state = await state.get_state()
    if not current_state:
        return

    data = await state.get_data()
    match getattr(BroadcastStates, current_state.split(':')[-1]):
        case BroadcastStates.add_broadcast_text:
            if not data.get('text'):
                await message.answer(await i18n_manager.get_translation(lang_code, "CANNOT_SKIP_STAGE"))
                return
            await message.answer("ENTER_BROADCAST_PHOTO")
            await state.set_state(BroadcastStates.add_broadcast_photo)
        case BroadcastStates.add_broadcast_photo:
            if not data.get('photo'):
                await state.update_data(photo=None)
            await message.answer(await i18n_manager.get_translation(lang_code, "ENTER_BROADCAST_BUTTONS"))
            await state.set_state(BroadcastStates.add_broadcast_button)
        case BroadcastStates.add_broadcast_button:
            if not data.get('buttons'):
                await state.update_data(buttons=None)
            await get_broadcast_response(message, state, lang_code)


@router.message(F.text, BroadcastStates.add_broadcast_text)
async def add_broadcast_text(message: Message, state: FSMContext):
    lang_code = await db.users_data.get_user_language(message.from_user.id)
    await state.update_data(text=message.text)
    await message.answer(await i18n_manager.get_translation(lang_code, "ENTER_BROADCAST_PHOTO"))
    await state.set_state(BroadcastStates.add_broadcast_photo)


@router.message(BroadcastStates.add_broadcast_photo)
async def add_broadcast_photo(message: Message, state: FSMContext):
    lang_code = await db.users_data.get_user_language(message.from_user.id)
    try:
        photo = message.photo[-1].file_id
    except:
        await message.answer(await i18n_manager.get_translation(lang_code, "INVALID_PHOTO_FORMAT"))
        return

    await state.update_data(photo=photo)
    await message.answer(await i18n_manager.get_translation(lang_code, "ENTER_BROADCAST_BUTTONS"))
    await state.set_state(BroadcastStates.add_broadcast_button)


@router.message(F.text, BroadcastStates.add_broadcast_button)
async def add_broadcast_button(message: Message, state: FSMContext):
    lang_code = await db.users_data.get_user_language(message.from_user.id)
    buttons = [[e.strip() for e in button_data.split('%%%')] for button_data in message.text.split('\n')]
    if any(len(btn) != 2 for btn in buttons):
        raise ValueError(await i18n_manager.get_translation(lang_code, "INVALID_BUTTON_FORMAT"))
    await state.update_data(buttons=buttons)
    await get_broadcast_response(message, state, lang_code)


def get_admin_broadcast_router():
    return router
