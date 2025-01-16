from .register import register_router
from .polls import poll_router
from .diary import diary_router
from .llm_handlers import gigachat_router

routers_list = [
    poll_router,
    register_router,
    diary_router,
    gigachat_router,
]

__all__ = [
    "routers_list",
]
