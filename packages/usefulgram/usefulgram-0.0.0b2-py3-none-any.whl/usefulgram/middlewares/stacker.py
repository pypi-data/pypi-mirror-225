

from typing import Dict, Any, Awaitable, Callable, Optional, Union

from aiogram import BaseMiddleware, Bot
from aiogram.types import TelegramObject, CallbackQuery, Message, Update

from usefulgram.exceptions import BotIsUndefined
from usefulgram.parsing.decode import DecodeCallbackData
from usefulgram.lazy import LazyEditor
from usefulgram.lazy import LazySender


class StackerMiddleware(BaseMiddleware):
    def __init__(self, stable: bool = False, separator: str = "/"):
        self.separator = separator
        self.stable = stable

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ):

        event_object: Union[CallbackQuery, Message]

        if not isinstance(event, (CallbackQuery, Message, Update)):
            raise await handler(event, data)

        if isinstance(event, Update):
            if event.message is not None:
                event_object = event.message

            elif event.callback_query is not None:
                event_object = event.callback_query

            else:
                raise await handler(event, data)

        else:
            event_object = event

        bot: Optional[Bot] = data.get("bot", None)

        if bot is None:
            raise BotIsUndefined

        data["sender"] = LazySender(
            event=event_object,
            bot=bot,
            stable=self.stable
        )

        if not isinstance(event_object, CallbackQuery):
            return await handler(event, data)

        data["decoder"] = DecodeCallbackData(
            callback_data=event_object.data,
            separator=self.separator
        )

        data["editor"] = LazyEditor(
            callback=event_object,
            bot=bot,
            stable=self.stable
        )

        return await handler(event, data)
