import asyncio

from typing import Union, Optional

from aiogram import Bot
from aiogram.types import (
    CallbackQuery,
    Message,
    FSInputFile,
    UNSET_PARSE_MODE,
    InlineKeyboardMarkup
)

from usefulgram.exceptions import MessageTooOld
from usefulgram.lazy.sender import MessageSender
from usefulgram.lazy.stable_wait import StableWaiter
from usefulgram.lazy.callback_responder import CallbackAnswer


class LazySender:
    _event: Union[CallbackQuery, Message]
    _bot: Bot
    _stable: bool

    def __init__(
            self,
            event: Union[CallbackQuery, Message],
            bot: Bot,
            stable: bool = False
    ):

        self._event = event
        self._bot = bot
        self._stable = stable

    @staticmethod
    def get_empty_text() -> str:
        spaces = " ⁣" * 65

        return f"⁣{spaces}⁣"

    async def send(
            self,
            text: Optional[str] = None,
            photo: Optional[FSInputFile] = None,
            video: Optional[FSInputFile] = None,
            reply_markup: Optional[InlineKeyboardMarkup] = None,
            parse_mode: Union[str] = UNSET_PARSE_MODE,
            disable_web_page_preview: bool = False,
            answer_text: Optional[str] = None,
            answer_show_alert: bool = False,
            autoanswer: bool = True
    ) -> Message:
        """
        Smart send menager

        :param text:
        :param photo:
        :param video:
        :param reply_markup:
        :param parse_mode:
        :param disable_web_page_preview:
        :param answer_text:
        :param answer_show_alert:
        :param autoanswer:
        :return:
        """

        if isinstance(self._event, CallbackQuery):
            if self._event.message is None:
                await self._event.answer("Message too old")

                raise MessageTooOld

            chat_id = self._event.message.chat.id
            thread_id = self._event.message.message_thread_id
            dt = self._event.message.date

        else:
            chat_id = self._event.chat.id
            thread_id = self._event.message_thread_id
            dt = self._event.date

        if self._stable:
            await asyncio.sleep(StableWaiter.get_stable_wait_time(dt))

        if text is None:
            text = self.get_empty_text()

        result = await MessageSender.send(
            bot=self._bot,
            chat_id=chat_id,
            text=text,
            message_thread_id=thread_id,
            photo=photo,
            video=video,
            reply_markup=reply_markup,
            parse_mode=parse_mode,
            disable_web_page_preview=disable_web_page_preview
        )

        if isinstance(self._event, CallbackQuery):
            await CallbackAnswer.auto_callback_answer(
                bot=self._bot,
                callback_id=self._event.id,
                autoanswer=autoanswer,
                answer_text=answer_text,
                answer_show_alert=answer_show_alert
            )

        return result
