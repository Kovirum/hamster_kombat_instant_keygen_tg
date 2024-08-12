from .commands import register_start_handler
from .callback_queries import register_callback_queries_handler


def register_handlers(dp):
    register_start_handler(dp)
    register_callback_queries_handler(dp)
