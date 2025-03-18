"""Модуль для встраивания логики в мидлварь."""
from aiogram import BaseMiddleware
from typing import Any, Callable, Dict, Awaitable
from aiogram.types import TelegramObject

class UserAcl(BaseMiddleware):
    """Class for realization acl"""
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        logging.info('UserAcl:\n'
                     'ACTION FROM USER: %s', data['event_from_user'])
        self.counter += 1
        data['counter'] = self.counter
        if data['event_from_user'].id in CONFIG['tg']['acl']:
            await handler(event, data)
        else:
            logging.info('UserAcl:\n'
                         'TELEGRAM ID %s IS NOT IN ACL', data['event_from_user'].id)