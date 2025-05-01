"""Определяет различные струкутры и классы для описания объектов в коде."""
from typing import List, Literal, Optional, Union
from enum import Enum
from pydantic import SecretStr, BaseModel, field_validator, Field


LogLevel = Literal['debug', 'info', 'warning', 'error', 'critical']


# class AccessList(BaseModel):
#     """
#     Список tg_id, у которых есть доступ к боту.
#     По дефолту список пустой, доступ к боту открыт всем.
#     """
#     tg_id: List[int] = []


class LogConfig(BaseModel):
    """Поля для настройки логгирования бота."""
    file_path: str = '/var/log/tg-template-test/bot.log'
    level: LogLevel = 'info'
    fmt: str = '%(asctime)s\t%(name)s\t%(levelname)s\t[%(filename)s:%(lineno)d]\t%(message)s'
    date_fmt: str = '%Y-%m-%dT%H:%M:%S'

    @field_validator('level')
    def validate_log_level(cls, value: LogLevel):
        """Проверка допустимого уровня логирования."""
        return value


class Config(BaseModel):
    """Класс для описания конфигурации и типов ее значений."""
    bot_token: SecretStr
    # acl: AccessList = AccessList()
    log: LogConfig = LogConfig()
    admin: List[int] = []

    @field_validator('bot_token')
    def validate_bot_token(cls, value: str):
        """Проверка на то, что bot_token не пустой."""
        if not value:
            raise ValueError('Bot token must not be empty!')
        return value


# Телеграм юзер
# https://core.telegram.org/constructor/user
class UserStatus(Enum):
    """Перечисление статусов телеграм юзера"""
    ONLINE = 0
    OFFLINE = 1
    RECENTLY = 2
    LAST_WEEK = 3
    LAST_MONTH = 4
    LONG_AGO = 5
    BOT = 6
    DELETED = 7
    PHONE_NUMBER_CONFIRMED = 8
    EMPTY = 9
