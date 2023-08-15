

import asyncio
from typing import Optional

from aiogram import Bot

from usefulgram.enums.const import Const


class CallbackAnswer:
    @staticmethod
    async def auto_callback_answer(
            bot: Bot,
            callback_id: str,
            autoanswer: bool = True,
            answer_text: Optional[str] = None,
            answer_show_alert: bool = False
    ) -> Optional[bool]:

        if not autoanswer:
            return None

        await asyncio.sleep(Const.SECONDS_BETWEEN_OPERATION)

        return await bot.answer_callback_query(
            callback_query_id=callback_id,
            text=answer_text,
            show_alert=answer_show_alert
        )
