"""Модуль для встраивания логики в мидлварь."""
from typing import Any, Awaitable, Callable, Dict
import pprint
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


USERS = {

}


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
        admins = self.config.admin
        permit_users = self.config.acl.permit
        deny_users = self.config.acl.deny

        user_tg_id = data['event_from_user'].id

        self.logger.info(
            'Action from user tg_id=%s', user_tg_id
        )

        if not USERS.get(data['event_from_user'].id):
            USERS[data['event_from_user'].id] = {
                'object': data['event_from_user'],
                'event_counter': 1,
            }
        else:
            USERS[data['event_from_user'].id]['event_counter'] += 1

        pprint.pprint(USERS)

        if not admins:
            if user_tg_id in admins:
                await handler(event, data)
                return

        if not deny_users:
            if user_tg_id in deny_users:
                self.logger.info(
                    'User with tg_id=%s is not in acl!', user_tg_id
                )
                return

        if not permit_users:
            if not user_tg_id in permit_users:
                self.logger.info(
                    'User with tg_id=%s is not in acl!', user_tg_id
                )
                return

        await handler(event, data)
