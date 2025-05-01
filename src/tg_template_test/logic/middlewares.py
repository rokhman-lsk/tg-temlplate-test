"""Модуль для встраивания логики в мидлварь."""
from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class UserAcl(BaseMiddleware):
    """Проверка юзера на вхождение в acl и инкрементирование счетчика действий юзера."""

    def __init__(self, logger, config):
        super().__init__()
        self.logger = logger
        self.config = config

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:

        if not USERS.get(data['event_from_user'].id):
            USERS[data['event_from_user'].id] = {
                'object': data['event_from_user'],
                'event_counter': 1,
            }
        else:
            USERS[data['event_from_user'].id]['event_counter'] += 1
        if not self.config.acl.tg_id:
            self.logger.info('ACL is empty!')
            await handler(event, data)
        else:
            if data['event_from_user'].id in self.config.acl.tg_id:
                await handler(event, data)
            else:
                self.logger.info('User (%s) is not in ACL!', data['event_from_user'])
        import pprint
        pprint.pprint(USERS)
