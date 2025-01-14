from .echo import echo_router
from .simple_menu import menu_router
from .register import register_router
from .polls import poll_router

routers_list = [
    poll_router,
    register_router,
]

__all__ = [
    "routers_list",
]
