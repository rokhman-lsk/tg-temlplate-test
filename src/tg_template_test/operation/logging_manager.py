"""Модуль управлением логгированием."""
import logging
from .config.pydantic_class import Config


def get_initial_logger(name: str = 'default_logger') -> logging.Logger:
    """
    Создаёт временный логгер без дополнительных настроек.

    Args:
        name (str): то самое название логгера
    Returns:
        logging.Logger: тот самый логгер
    """
    logger = logging.getLogger(name)
    logger.setLevel('INFO')
    logger.handlers.clear()
    formatter = logging.Formatter(
            fmt = '%(asctime)s\t%(name)s\t%(levelname)s\t[%(filename)s:%(lineno)d]\t%(message)s',
            datefmt='%Y-%m-%dT%H:%M:%S'
        )
    if not logger.hasHandlers():
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

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
            fmt = config.log.fmt,
            datefmt=config.log.date_fmt
        )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    log_file = config.log.file_path
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
