from aiogram import F, types, Router, html
from aiogram.utils.formatting import as_list, Bold, as_numbered_section, Code

from bot.logic import send_menu_reponse, check_user_channel_subscription
from bot.keyboards import subcheck_markup, delmsg_markup
from common.database import db
from common.tools.utils import get_date
from config import GamePromoTypes

router = Router()


@router.callback_query(F.data == 'check_subscription')
async def check_subscription(callback: types.CallbackQuery):
    access = await check_user_channel_subscription(callback.bot, callback.from_user.id)
    if not access:
        await callback.answer(text='You have not subscribed to the channel',
                              show_alert=True)
    else:
        await callback.answer(text="The subscription is confirmed. Enjoy your use.",
                              show_alert=True)
        await callback.message.delete()
        await send_menu_reponse(callback.message, callback.from_user.id)


@router.callback_query(F.data.in_([game.value for game in GamePromoTypes]))
async def get_game_key_handler(callback: types.CallbackQuery):
    access = await check_user_channel_subscription(callback.bot, callback.from_user.id)
    if not access:
        await callback.message.answer(
            f"You must subscribe to channel to use the bot",
            reply_markup=subcheck_markup)
    else:
        game = GamePromoTypes.__getitem__(callback.data)
        user_available_keys, _ = await db.users_data.get_pool_limit(game, callback.from_user.id)
        game_key_pool_limit = await db.keys_pool.count_key_pool(game)

        if game_key_pool_limit <= 0:
            return await callback.answer("The key pool for this game is empty. try again later", show_alert=True)
        if user_available_keys <= 0:
            return await callback.answer("You have reached today's key limit for this game", show_alert=True)

        key = await db.keys_pool.get_key(game)
        await db.users_data.count_key_receive(game, callback.from_user.id, key)

        await callback.message.answer(f"The key to the game \"{callback.data}\": {html.code(key)}",
                                      reply_markup=delmsg_markup)
        await callback.answer()


@router.callback_query(F.data == "update_menu")
async def update_menu_handler(callback: types.CallbackQuery):
    try:
        await callback.message.delete()
        await send_menu_reponse(callback.message, callback.from_user.id)
        await callback.answer()
    except Exception as e:
        await callback.answer(f"Failed to update menu: {e}", show_alert=True)


@router.callback_query(F.data == 'delete_message')
async def delete_message_handler(callback: types.CallbackQuery):
    try:
        await callback.message.delete()
    except Exception as e:
        await callback.answer(text=f"The message could not be deleted: {e}", show_alert=True)


@router.callback_query(F.data == 'history_menu')
async def history_menu_handler(callback: types.CallbackQuery):
    history_data = await db.users_data.get_history_data(callback.from_user.id)
    response = as_list(
        Bold(f"Key collection history ({get_date()})\n"),
        *[as_numbered_section(Bold(game.value), *[Code(key)
                                                  for key in history_data.get(game.value) or ['Empty']])
          for game in GamePromoTypes
          ],
        sep='\n\n'
    )
    await callback.message.answer(text=response.as_html(), reply_markup=delmsg_markup)
    await callback.answer()


def register_callback_queries_handler(dp):
    dp.include_router(router)
