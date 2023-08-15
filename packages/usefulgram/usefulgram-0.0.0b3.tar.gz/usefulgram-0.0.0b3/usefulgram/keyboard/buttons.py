

from typing import Optional, Any, Union

from aiogram.types import (
    InlineKeyboardButton,
    KeyboardButton,
    WebAppInfo,
    KeyboardButtonRequestChat,
    KeyboardButtonRequestUser,
    KeyboardButtonPollType,
    SwitchInlineQueryChosenChat,
    LoginUrl,
    CallbackGame
)

from usefulgram.parsing.encode import CallbackData


class Button(InlineKeyboardButton):
    def __init__(
            self,
            text: Union[str, int],
            *args: Any,
            prefix: Optional[str] = None,
            url: Optional[str] = None,
            callback_game: Optional[CallbackGame] = None,
            login_url: Optional[LoginUrl] = None,
            pay: Optional[bool] = None,
            switch_inline_query: Optional[str] = None,
            switch_inline_query_chosen_chat: Optional[
                SwitchInlineQueryChosenChat
            ] = None,
            switch_inline_query_current_chat: Optional[str] = None,
            separator: str = "/",
    ):
        prefix = self._get_prefix(prefix, args)

        if isinstance(text, int):
            text = str(text)

        if prefix is not None:
            callback_data = CallbackData(prefix, *args, separator=separator)

        else:
            callback_data = None

        super().__init__(
            text=text,
            url=url,
            callback_data=callback_data,
            callback_game=callback_game,
            login_url=login_url,
            pay=pay,
            switch_inline_query=switch_inline_query,
            switch_inline_query_chosen_chat=switch_inline_query_chosen_chat,
            switch_inline_query_current_chat=switch_inline_query_current_chat,
        )

    @staticmethod
    def _get_prefix(prefix: Optional[str], args: tuple[Any, ...]) -> Optional[str]:
        if prefix is not None:
            return prefix

        for obj in args:
            result = obj.__getattribute__("prefix")

            if result is not None:
                return result

        return None


class ReplyButton(KeyboardButton):
    def __init__(
            self,
            text: str,
            web_app: Optional[WebAppInfo] = None,
            request_chat: Optional[KeyboardButtonRequestChat] = None,
            request_user: Optional[KeyboardButtonRequestUser] = None,
            request_contact: Optional[bool] = None,
            request_poll: Optional[KeyboardButtonPollType] = None
    ):
        super().__init__(
            text=text,
            web_app=web_app,
            request_chat=request_chat,
            request_user=request_user,
            request_contact=request_contact,
            request_poll=request_poll
        )
