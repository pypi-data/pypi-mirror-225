

import asyncio

from typing import Optional, Union
from datetime import datetime, timedelta
import pytz

from aiogram.types import (
    CallbackQuery,
    Message,
    FSInputFile,
    InlineKeyboardMarkup,
    UNSET_PARSE_MODE,
)

from aiogram import Bot
from aiogram.enums.chat_type import ChatType

from usefulgram.enums import Const
from usefulgram.exceptions import MessageTooOld
from usefulgram.lazy.editor import MessageEditor
from usefulgram.lazy.sender import MessageSender
from usefulgram.lazy.stable_wait import StableWaiter
from usefulgram.lazy.callback_responder import CallbackAnswer


class LazyEditor:
    _callback: CallbackQuery
    _bot: Bot
    _stable: bool

    def __init__(self, callback: CallbackQuery, bot: Bot, stable: bool = False):
        self._callback = callback
        self._bot = bot
        self._stable = stable

    @staticmethod
    def _get_text_by_caption(
            text: Optional[str],
            caption: Optional[str]
    ) -> Optional[str]:

        if text is None or caption is not None:
            return caption

        return text

    @staticmethod
    def _get_message_text(text: Optional[str], message: Message) -> Optional[str]:
        if text is None:
            return message.text

        return text

    @staticmethod
    def _get_data_changes_status(
            message: Message,
            text: Optional[str],
            reply_markup: Optional[InlineKeyboardMarkup],
            video: Optional[FSInputFile],
            photo: Optional[FSInputFile],
    ) -> bool:

        media = photo or video

        if message.text != text:
            return True

        if message.reply_markup != reply_markup:
            return True

        if media:
            return True

        return False

    @staticmethod
    def _get_delta_between_current_and_message(
            message_date: datetime
    ) -> timedelta:

        current = datetime.now(tz=pytz.UTC)

        return current - message_date

    @staticmethod
    def _get_time_allowed_edit_status(message: Message) -> bool:
        const_delta = timedelta(hours=Const.ALLOW_EDITING_DELTA)

        delta = LazyEditor._get_delta_between_current_and_message(
            message.date
        )

        return delta < const_delta

    @staticmethod
    def _get_message_in_chat_status(message: Message) -> bool:
        if message.chat.type == ChatType.CHANNEL:
            return True

        return False

    @staticmethod
    def _get_message_media_is_correct_status(
            message: Message,
            photo: Optional[FSInputFile],
            video: Optional[FSInputFile]
    ) -> bool:

        message_has_media = message.photo or message.video
        media = photo or video

        if media and not message_has_media:
            return False

        if not media and message_has_media:
            return False

        return True

    def _get_bot_allow_edit_status(
            self,
            message: Message,
            photo: Optional[FSInputFile],
            video: Optional[FSInputFile],
    ) -> bool:

        if self._get_message_in_chat_status(message):
            return True

        if not self._get_time_allowed_edit_status(message):
            return False

        if not self._get_message_media_is_correct_status(
            message=message, photo=photo, video=video
        ):
            return False

        return True

    @staticmethod
    async def _send_or_edit(
            bot: Bot,
            can_edit: bool,
            message: Message,
            text: Optional[str],
            photo: Optional[FSInputFile],
            video: Optional[FSInputFile],
            reply_markup: Optional[InlineKeyboardMarkup],
            parse_mode: Union[str],
            disable_web_page_preview: bool,
            on_onflict_do_nothing: bool
    ) -> Union[Message, bool]:

        if not can_edit:
            if on_onflict_do_nothing:
                return False

            text = LazyEditor._get_message_text(text, message=message)

            return await MessageSender.send(
                bot=bot,
                chat_id=message.chat.id,
                message_thread_id=message.message_thread_id,
                text=text,
                photo=photo,
                video=video,
                reply_markup=reply_markup,
                parse_mode=parse_mode,
                disable_web_page_preview=disable_web_page_preview
            )

        return await MessageEditor.edit(
            bot=bot,
            chat_id=message.chat.id,
            message_id=message.message_id,
            text=text,
            photo=photo,
            video=video,
            reply_markup=reply_markup,
            parse_mode=parse_mode,
            disable_web_page_preview=disable_web_page_preview
        )

    def _get_can_edit_status(
            self,
            message: Message,
            photo: Optional[FSInputFile],
            video: Optional[FSInputFile],
    ) -> bool:

        if message is None:
            return False

        if not self._get_bot_allow_edit_status(
                message=message,
                photo=photo,
                video=video
        ):
            return False

        return True

    @staticmethod
    def _get_stable_wait_time(message: Message) -> float:
        if message.edit_date:
            dt = datetime.fromtimestamp(message.edit_date, tz=pytz.UTC)

        else:
            dt = message.date

        return StableWaiter.get_stable_wait_time(dt)

    async def edit(
            self,
            text: Optional[str] = None,
            photo: Optional[FSInputFile] = None,
            video: Optional[FSInputFile] = None,
            reply_markup: Optional[InlineKeyboardMarkup] = None,
            parse_mode: Union[str, UNSET_PARSE_MODE] = UNSET_PARSE_MODE,
            disable_web_page_preview: bool = False,
            on_onflict_do_nothing: bool = False,
            answer_text: Optional[str] = None,
            answer_show_alert: bool = False,
            autoanswer: bool = True
    ) -> Union[Message, bool]:
        """
        Smart edit menager
        :param text: edit message text
        :param photo: edit message media
        :param video: edit message media
        :param reply_markup: edit message inline keyboard object
        :param parse_mode: Mode for parsing entities in the message text.
        See formatting options for more details.
        :param disable_web_page_preview:
        :param on_onflict_do_nothing:
        :param answer_text: if autoanser, it got callback.answer()
        :param answer_show_alert: if autoanser, it got callback.answer()
        :param autoanswer: should menager calls callback.answer()
        :return:
        """

        callback = self._callback
        message = callback.message

        if message is None:
            await callback.answer("Message too old")

            raise MessageTooOld

        if self._stable:
            await asyncio.sleep(self._get_stable_wait_time(message))

        if not self._get_data_changes_status(
                message=message,
                text=text,
                reply_markup=reply_markup,
                video=video,
                photo=photo,
        ):
            return message

        can_edit = self._get_can_edit_status(
            message=message,
            photo=photo,
            video=video,
        )

        result = await self._send_or_edit(
            bot=self._bot,
            can_edit=can_edit,
            message=message,
            text=text,
            photo=photo,
            video=video,
            reply_markup=reply_markup,
            parse_mode=parse_mode,
            disable_web_page_preview=disable_web_page_preview,
            on_onflict_do_nothing=on_onflict_do_nothing
        )

        await CallbackAnswer.auto_callback_answer(
            bot=self._bot,
            callback_id=callback.id,
            autoanswer=autoanswer,
            answer_text=answer_text,
            answer_show_alert=answer_show_alert
        )

        return result
