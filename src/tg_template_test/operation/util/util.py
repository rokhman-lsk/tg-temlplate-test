"""Модуль для различных скриптов, полезных функций"""
import os
from typing import Dict, Any
from logging import Logger
from pydantic import BaseModel


def pydantic_obj_to_dict_recursive(logger: Logger, obj: BaseModel) -> Dict[str, Any]:
    """
    Конвертация необходимых полей pydantic объекта в словарь.
    Args:
        logger (Logger): логгер
        obj (BaseModel): ожидает pydantic объект, который описывает конфигурацию
    Returns:
        Dict[str]:
            возвращает словарь после обработки pydantic объекта
    """
    logger.debug('Serializing pydantic obj into dict...')
    data = obj.model_dump()
    for key, value in data.items():
        if isinstance(value, BaseModel):
            data[key] = pydantic_obj_to_dict_recursive(value, logger)
    return data


def check_and_create_file(logger: Logger, file_path: str) -> bool:
    """
    Проверяет наличие прав на запись в файл.
    Если файла нет, то создает его.
    Args:
        logger (Logger): логгер
        file_path (str): путь к файлу
    Returns:
        bool:
            возвращает True, если есть права на запись,
            или если файл успешно создан, в противном случае False
    """
    logger.debug('Check existance and permission file %s', file_path)
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        if not os.path.exists(file_path):
            with open(file_path, 'w', encoding='utf-8'):
                pass
            logger.debug('File %s has been created', file_path)
            return True
        if os.access(file_path, os.W_OK):
            logger.debug('File %s exists, permissions are ok', file_path)
            return True
        return False
    except (OSError, PermissionError):
        return False