"""Модуль управлением конфигурацией"""
import sys
import yaml
from class_definition import Config
from logging_manager import get_initial_logger


logger = get_initial_logger()


def read_config(file_path: str) -> Config:
    """
    Парсит и отдает конфигурацию.

    Args:
        file_path (str): путь к файлу конфигурации
    Returns:
        Config: pydantic объект конфига
    """
    try:
        logger.info('Reading config...')
        with open(file_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        logger.fatal("Config doesn't exists!")
        sys.exit(1)
    except PermissionError:
        logger.fatal('Config is not readable!')
        sys.exit(1)
    return Config(**config)
