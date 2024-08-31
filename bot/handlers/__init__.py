from .commands import register_commands_handler
from .callback_queries import register_callback_queries_handler
from .admin import register_admin_handler


def register_handlers(dp):
    register_commands_handler(dp)
    register_callback_queries_handler(dp)
    register_admin_handler(dp)
