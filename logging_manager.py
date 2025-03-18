"""Модуль управлением логгированием."""
import sys
import logging
from class_definition import Config


def get_initial_logger(name: str = 'default_logger') -> logging.Logger:
    """
    Создаёт временный логгер без дополнительных настроек.

    Args:
        name (str): то самое название логгера
    Returns:
        logging.Logger: тот самый логгер
    """
    logger = logging.getLogger(name)
    logger.setLevel('DEBUG')
    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter(
                fmt = \
                '%(asctime)s\t%(name)s\t%(levelname)s\t[%(filename)s:%(lineno)d]\t%(message)s',
                datefmt='%Y-%m-%dT%H:%M:%S'
            )
        )
        logger.addHandler(handler)
    return logger


def get_configure_logger(config: Config, name: str = 'configured_logger') -> logging.Logger:
    """
    Настраивает логгер на основе переданной конфигурации
    (путь к файлу, уровень логгирования и т.д.).

    Args:
        config (Setting): тот самый конфиг
        name (str): то самое название логгера
    Returns:
        logging.Logger: тот самый логгер
    """
    logger = logging.getLogger(name)
    logger.setLevel(config.log.level.upper())
    logger.handlers.clear()
    formatter = logging.Formatter(
            fmt = \
            '%(asctime)s\t%(name)s\t%(levelname)s\t[%(filename)s:%(lineno)d]\t%(message)s',
            datefmt='%Y-%m-%dT%H:%M:%S'
        )

    log_file = config.log.file_path
    if log_file:
        handler = logging.FileHandler(log_file)
    else:
        handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    if sys.stdin.isatty():
        handler_isatty = logging.StreamHandler()
        handler_isatty.setFormatter(formatter)
    logger.addHandler(handler)
    logger.addHandler(handler_isatty)

    return logger
