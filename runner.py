"""Точка входа в приложение."""
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from config_reader import read_config
from logging_manager import get_configure_logger
from common import start, echo


async def main() -> None:
    """Main."""
    config = read_config('./config.yaml')
    logger = get_configure_logger(config)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(start.router)
    dp.include_router(echo.router)
    bot = Bot(
        token=config.bot_token.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info('Running bot...')
    await dp.start_polling(bot)


if __name__ == "__main__":
    #logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
