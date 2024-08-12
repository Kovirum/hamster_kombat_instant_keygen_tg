from aiogram import types, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.utils.formatting import as_list, as_marked_section, as_key_value, Bold
from app.checkers import check_user_channel_subscription
from config import GamePromoTypes
from database import db

from app.keyboards import menu_markup, subcheck_markup

router = Router()


async def menu(message: types.Message, user_id: int):
    response = as_list(
        as_marked_section(
            Bold("Total keys in the pool"),
            *[as_key_value(game.value, await db.keys_pool.count_key_pool(game)) for game in GamePromoTypes]
        ),
        as_marked_section(
            Bold("Available daily keys"),
            *[
                as_key_value(
                    game.value,
                    '/'.join(map(str, await db.users_data.get_pool_limit(game, user_id)))
                )
                for game in GamePromoTypes
            ]
        ),
        sep='\n\n'
    )
    await message.answer(response.as_html(), reply_markup=menu_markup)


@router.message(Command('start'))
async def send_welcome(message: types.Message):
    access = await check_user_channel_subscription(message.bot, message.from_user.id)
    if not access:
        await message.answer(
            f"You must subscribe to channel to use the bot",
            reply_markup=subcheck_markup)
    else:
        await menu(message, message.from_user.id)


def register_start_handler(dp):
    dp.include_router(router)
