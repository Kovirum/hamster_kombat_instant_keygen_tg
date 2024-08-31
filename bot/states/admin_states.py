from aiogram.fsm.state import StatesGroup, State


class BroadcastStates(StatesGroup):
    add_broadcast_text = State()
    add_broadcast_photo = State()
    add_broadcast_button = State()
