"""Точка входа в приложение."""
import sys
import argparse
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from .operation.config.pydantic_class import Config
from .operation.config.reader import read_config
from .operation.logging_manager import get_initial_logger, get_configure_logger
from .operation.constants import EPILOG
from .logic.common import start, echo
from .logic.middlewares import UserAcl

logger = get_initial_logger()
logger.debug('Start...')

def get_parser() -> argparse.ArgumentParser:
    """
    Создает объект парсер, добавляет необходимые аргументы и возвращает его.
    Returns:
        argparse.ArgumentParser: тот самый парсер
    """
    logger.debug('Creating parser...')
    parser = argparse.ArgumentParser(
        prog='tg-template-bot',
        description='The template telegram bot',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=EPILOG
    )
    parser.add_argument(
        '-c',
        '--config',
        help='Launch telegram bot with config',
        required=True,
    )
    parser.add_argument(
        '--log-level',
        type=str,
        help='Determines the logging level before reading the configuration '\
             '(debug, info, warning, error)',
    )
    return parser


def handling_arguments(args: argparse.Namespace) -> Config:
    """
    Точка входа для обработки аргументов.
    Args:
        parser (argparse.ArgumentParser): те самые аргументы"""
    logger.debug('Parsing arguments...')
    if args.log_level:
        if args.log_level in ('debug', 'info', 'warning', 'error'):
            logger.setLevel(args.log_level.upper())
    if args.config:
        config = read_config(logger, args.config)
    else:
        logger.critical('Config file must be specified!')
        sys.exit(1)
    logger.info('Config found: %s', args.config)
    return config


async def main() -> None:
    """Main."""
    parser = get_parser()
    args = parser.parse_args()
    config = handling_arguments(args)
    configured_logger = get_configure_logger(config)

    dp = Dispatcher(storage=MemoryStorage())
    dp.update.outer_middleware(UserAcl(logger=logger, config=config))

    dp.include_router(start.router)
    dp.include_router(echo.router)

    bot = Bot(
        token=config.bot_token.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    await bot.delete_webhook(drop_pending_updates=True)
    configured_logger.info('Running bot...')
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
