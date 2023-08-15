

from typing import Optional, Union, Coroutine, Any

from aiogram.types import (
    Message,
    FSInputFile,
    InlineKeyboardMarkup,
    UNSET_PARSE_MODE,
)

from aiogram import Bot

from usefulgram.exceptions import MessageTextIsNone


class MessageSender:
    @staticmethod
    def send(
            bot: Bot,
            chat_id: int,
            text: Optional[str],
            message_thread_id: Optional[int] = None,
            photo: Optional[FSInputFile] = None,
            video: Optional[FSInputFile] = None,
            reply_markup: Optional[InlineKeyboardMarkup] = None,
            parse_mode: Union[str] = UNSET_PARSE_MODE,
            disable_web_page_preview: bool = False,
    ) -> Coroutine[Any, Any, Message]:

        if photo is not None:
            return bot.send_photo(
                chat_id=chat_id,
                message_thread_id=message_thread_id,
                photo=photo,
                caption=text,
                reply_markup=reply_markup,
                parse_mode=parse_mode,
            )

        if video is not None:
            return bot.send_video(
                chat_id=chat_id,
                message_thread_id=message_thread_id,
                video=video,
                caption=text,
                reply_markup=reply_markup,
                parse_mode=parse_mode,
            )

        if text is None:
            raise MessageTextIsNone

        return bot.send_message(
            chat_id=chat_id,
            message_thread_id=message_thread_id,
            text=text,
            reply_markup=reply_markup,
            parse_mode=parse_mode,
            disable_web_page_preview=disable_web_page_preview
        )
