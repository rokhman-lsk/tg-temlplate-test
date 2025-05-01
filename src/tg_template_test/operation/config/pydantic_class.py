"""Определяет различные струкутры и классы для предствления конфигурации в виде объектов."""
from typing import List, Literal
from typing_extensions import Self
from enum import Enum
from pydantic import SecretStr, BaseModel, field_validator, model_validator



LogLevel = Literal['debug', 'info', 'warning', 'error', 'critical']


class AccessList(BaseModel):
    """
    Список tg_id, у которых есть доступ к боту и у которых его нет.
    По дефолту список пустой, доступ к боту открыт всем.
    """
    permit: List[int] = []
    deny: List[int] = []

    @model_validator(mode='after')
    def validate_acl(self) -> Self:
        """Проверка на то, что permit и deny не определены одновременно."""
        if self.permit and self.deny:
            raise ValueError("Fields 'permit', 'deny' are mutually exclusive")
        return self


class LogConfig(BaseModel):
    """Поля для настройки логгирования бота."""
    file_path: str = '/var/log/tg-template-test/bot.log'
    level: LogLevel = 'info'
    fmt: str = '%(asctime)s\t%(name)s\t%(levelname)s\t[%(filename)s:%(lineno)d]\t%(message)s'
    date_fmt: str = '%Y-%m-%dT%H:%M:%S'


class Config(BaseModel):
    """Класс для описания конфигурации."""
    bot_token: SecretStr
    admin: List[int] = []
    acl: AccessList = AccessList()
    log: LogConfig = LogConfig()

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
