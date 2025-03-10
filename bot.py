import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage, SimpleEventIsolation
from apscheduler.schedulers.asyncio import AsyncIOScheduler  # type: ignore

from infrastructure.database.setup import create_engine, create_session_pool
from tgbot.config import Config, load_config
from tgbot.handlers import routers_list
from tgbot.middlewares import ConfigMiddleware, DatabaseMiddleware
from tgbot.services.scheduler import send_periodic_message


async def on_startup(bot: Bot):
    return


def register_global_middlewares(dp: Dispatcher, config: Config):
    """
    Register global middlewares for the given dispatcher.
    Global middlewares here are the ones that are applied to all the handlers (you specify the type of update)

    :param dp: The dispatcher instance.
    :type dp: Dispatcher
    :param config: The configuration object from the loaded configuration.
    :return: None
    """
    middleware_types = [
        ConfigMiddleware(config),
        DatabaseMiddleware(create_session_pool(create_engine(config.db))),
    ]

    for middleware_type in middleware_types:
        dp.message.outer_middleware(middleware_type)
        dp.callback_query.outer_middleware(middleware_type)


def setup_logging():
    """
    Set up logging configuration for the application.

    This method initializes the logging configuration for the application.
    It sets the log level to INFO and configures a basic colorized log for
    output. The log format includes the filename, line number, log level,
    timestamp, logger name, and log message.

    Returns:
        None

    Example usage:
        setup_logging()
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )
    logger = logging.getLogger(__name__)
    logger.info("Starting bot")


def get_storage(config):
    """
    Return storage based on the provided configuration.

    Args:
        config (Config): The configuration object.

    Returns:
        Storage: The storage object based on the configuration.

    """
    return MemoryStorage()


def run_scheduler_tasks(bot: Bot, scheduler: AsyncIOScheduler):
    scheduler.add_job(send_periodic_message, "interval", seconds=15, args=[bot])
    scheduler.start()
    logging.info("Scheduler started")


async def main():
    setup_logging()

    config = load_config(".env")
    storage = get_storage(config)

    bot = Bot(token=config.tg_bot.token, default=DefaultBotProperties())
    dp = Dispatcher(storage=storage, events_isolation=SimpleEventIsolation())

    dp.include_routers(*routers_list)

    register_global_middlewares(dp, config)

    scheduler = AsyncIOScheduler()
    run_scheduler_tasks(bot, scheduler)

    await on_startup(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot has stopped!")
    finally:
        logger = logging.getLogger(__name__)
        logger.info("Bot stopped")
