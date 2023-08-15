

"""
This code based on
https://github.com/wakaree/simple_echo_bot/blob/main/middlewares/throttling.py
"""

from typing import Callable, Dict, Any, Awaitable, MutableMapping, Optional

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User

from cachetools import TTLCache

from usefulgram.exceptions import Throttling


class ThrottlingMiddleware(BaseMiddleware):
    RATE_LIMIT = 0.7
    SIMPLE = True

    def __init__(
            self, rate_limit: float = RATE_LIMIT, simple: bool = SIMPLE
    ) -> None:

        self._cache: MutableMapping[int, None] = TTLCache(
            maxsize=10_000, ttl=rate_limit
        )

        self.SIMPLE = simple

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Optional[Any]:
        user: Optional[User] = data.get("event_from_user", None)

        if user is not None:
            if user.id in self._cache:
                self._cache[user.id] = None

                if self.SIMPLE:
                    return None

                raise Throttling()

            self._cache[user.id] = None

        return await handler(event, data)
