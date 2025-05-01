"""Модуль парсинга конфигурации."""
import sys
from logging import Logger
import yaml
from .pydantic_class import Config
from ..util.util import check_and_create_file


def read_config(logger: Logger, file_path: str) -> Config:
    """
    Парсит и отдает конфигурацию.

    Args:
        logger (Logger): логгер
        file_path (str): путь к файлу конфигурации
    Returns:
        Config: pydantic объект конфига
    """
    logger.info('Reading config...')

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
    except (OSError, PermissionError):
        logger.error("Config isn't readable!")
        sys.exit(1)

    config = Config(**config)

    logger.info('Checking log file...')

    log_file = config.log.file_path
    if check_and_create_file(logger, log_file) is False:
        logger.error("Сan't create log file!")
        sys.exit(1)

    return config
