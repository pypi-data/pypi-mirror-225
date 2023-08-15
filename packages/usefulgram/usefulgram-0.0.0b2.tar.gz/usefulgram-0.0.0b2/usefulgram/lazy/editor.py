
from typing import Optional, Union, Coroutine, Any

from aiogram.types import (
    Message,
    InputMediaPhoto,
    InputMediaVideo,
    FSInputFile,
    InlineKeyboardMarkup,
    UNSET_PARSE_MODE,
)

from aiogram import Bot

from usefulgram.exceptions import CantEditMedia


class MessageEditor:
    @staticmethod
    def edit(
            bot: Bot,
            chat_id: int,
            message_id: int,
            text: Optional[str] = None,
            photo: Optional[FSInputFile] = None,
            video: Optional[FSInputFile] = None,
            reply_markup: Optional[InlineKeyboardMarkup] = None,
            parse_mode: Union[str] = UNSET_PARSE_MODE,
            disable_web_page_preview: bool = False
    ) -> Coroutine[Any, Any, Union[Message, bool]]:

        if photo or video:
            media: Union[InputMediaVideo, InputMediaPhoto]

            if photo:
                media = InputMediaPhoto(
                    media=photo,
                    caption=text,
                    parse_mode=parse_mode
                )

            elif video:
                media = InputMediaVideo(
                    media=video,
                    caption=text,
                    parse_mode=parse_mode
                )

            else:
                raise CantEditMedia

            return bot.edit_message_media(
                chat_id=chat_id,
                message_id=message_id,
                media=media,
                reply_markup=reply_markup,
            )

        if text is None:
            return bot.edit_message_reply_markup(
                chat_id=chat_id,
                message_id=message_id,
                reply_markup=reply_markup,
            )

        return bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            reply_markup=reply_markup,
            parse_mode=parse_mode,
            disable_web_page_preview=disable_web_page_preview
        )
