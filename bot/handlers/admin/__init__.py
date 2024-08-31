from .admin_menu import get_admin_menu_router
from .broadcast_menu import get_admin_broadcast_router


def register_admin_handler(dp):
    dp.include_router(get_admin_menu_router())
    dp.include_router(get_admin_broadcast_router())
