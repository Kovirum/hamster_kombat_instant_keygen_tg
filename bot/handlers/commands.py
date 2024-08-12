from aiogram import types, Router
from aiogram.filters import Command
from bot.logic import send_menu_reponse, check_user_channel_subscription

from bot.keyboards import subcheck_markup

router = Router()


@router.message(Command("menu"))
async def open_menu(message: types.Message):
    access = await check_user_channel_subscription(message.bot, message.from_user.id)
    if not access:
        await message.answer(
            f"You must subscribe to channel to use the bot",
            reply_markup=subcheck_markup)
    else:
        await send_menu_reponse(message, message.from_user.id)


@router.message(Command('start'))
async def send_welcome(message: types.Message):
    await message.answer("UNDER DEVELOPMENT. USE /menu command")

    # TODO:
    # language selector response logic
    # language selector keyboard (ru/en)
    # i18n manager (ujson + aiofiles)
    # subscibe_check_response func


@router.message(Command('language'))
async def language_choice(message: types.Message):
    await message.answer("UNDER DEVELOPMENT.")

    # TODO:
    # command logic


def register_start_handler(dp):
    dp.include_router(router)
