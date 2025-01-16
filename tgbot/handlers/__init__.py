from .simple_menu import menu_router
from .register import register_router
from .polls import poll_router
from .llm_handlers import gigachat_router

routers_list = [
    poll_router,
    register_router,
    gigachat_router,
]

__all__ = [
    "routers_list",
]
