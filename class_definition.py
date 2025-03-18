"""Определяет различные струкутры и классы для описания объектов в коде."""
from typing import List, Literal
from pydantic import SecretStr, BaseModel, field_validator

# Конфигурация бота

class AccessList(BaseModel):
    """
    Список tg_id, у которых есть доступ к боту.
    По дефолту список пустой, доступ к боту открыт всем.
    """
    tg_id: List[int] = []

LogLevel = Literal['debug', 'info', 'warning', 'error', 'critical']

class LogConfig(BaseModel):
    """Поля для настройки логгирования бота."""
    file_path: str = './tg-bot.log'
    level: LogLevel = 'info'

    @field_validator('level')
    def validate_log_level(cls, value: LogLevel):
        """Проверка допустимого уровня логирования."""
        return value

class Config(BaseModel):
    """Класс для описания конфигурации и типов ее значений."""
    bot_token: SecretStr
    acl: AccessList = AccessList()
    log: LogConfig = LogConfig()

    @field_validator('bot_token')
    def validate_bot_token(cls, value: str):
        """Проверка на то, что bot_token не пустой."""
        if not value:
            raise ValueError('Bot token must not be empty!')
        return value
