from .register import register_router
from .polls import poll_router
from .diary import diary_router
from .llm_handlers import gigachat_router
from .help import help_router
from .wrong_command import wrong_command_router

routers_list = [
    poll_router,
    register_router,
    diary_router,
    help_router,
    wrong_command_router,
    gigachat_router,
]

__all__ = [
    "routers_list",
]
