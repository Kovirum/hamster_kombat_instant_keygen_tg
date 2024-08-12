from aiogram import types
from aiogram.utils.formatting import as_list, as_marked_section, Bold, as_key_value

from bot.keyboards import menu_markup
from common.database import db
from config import GamePromoTypes


async def send_menu_reponse(message: types.Message, user_id: int):
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
