from .echo import echo_router
from .simple_menu import menu_router
from .register import register_router
from .llm_handlers import gigachat_router

routers_list = [
    menu_router,
    register_router,
    echo_router,
    gigachat_router,
]

__all__ = [
    "routers_list",
]
