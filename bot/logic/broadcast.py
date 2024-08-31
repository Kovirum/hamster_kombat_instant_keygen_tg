import asyncio
import aiogram.types
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from bot.i18n import i18n_manager
from common.database import db

from bot.keyboards import get_broadcast_buttons_markup, get_broadcast_final_markup


async def get_broadcast_response(message: Message, state: FSMContext, lang_code):
    await state.set_state(None)
    await message.answer(await i18n_manager.get_translation(lang_code, "BROADCAST_MESSAGE_CREATED"))
    data = await state.get_data()
    await send_broadcast_message(message.bot, message.chat.id, data)
    await message.answer(
        text=await i18n_manager.get_translation(lang_code, "CONFIRM_ACTION_PROMPT"),
        reply_markup=await get_broadcast_final_markup(lang_code))


async def send_broadcast_message(bot: aiogram.Bot, chat_id: int, data: dict):
    if data.get("photo"):
        await bot.send_photo(
            chat_id=chat_id,
            photo=data["photo"],
            caption=data["text"],
            reply_markup=get_broadcast_buttons_markup(data['buttons']) if data['buttons'] else None
        )
    else:
        await bot.send_message(
            chat_id=chat_id,
            text=data["text"],
            reply_markup=get_broadcast_buttons_markup(data['buttons']) if data['buttons'] else None
        )


async def start_broadcast(message: Message, state: FSMContext):
    lang_code = await db.users_data.get_user_language(message.from_user.id)
    data = await state.get_data()
    await state.clear()

    user_ids = await db.users_data.get_users_for_broadcast()
    await message.answer(
        text=(await i18n_manager.get_translation(lang_code, "BROADCAST_STARTED")).format(count=len(user_ids)))

    # This is bad, but so far so
    cnt = 0
    for user_id in user_ids:
        try:
            await send_broadcast_message(message.bot, user_id, data)
            cnt += 1
        except:
            pass
        await asyncio.sleep(0.2)

    await message.answer(
        text=(await i18n_manager.get_translation(lang_code, "BROADCAST_ENDED")).format(
            count_received=cnt,
            total_users=len(user_ids)))
