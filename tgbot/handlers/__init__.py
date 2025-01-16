from .echo import echo_router
from .simple_menu import menu_router
from .register import register_router
from .polls import poll_router
from .diary import diary_router

routers_list = [
    poll_router,
    register_router,
    diary_router,
]

__all__ = [
    "routers_list",
]
