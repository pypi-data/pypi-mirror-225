
from typing import Optional, Any, TypeVar

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from usefulgram.keyboard.rows import Row, ReplyRow


T = TypeVar("T")


class BaseBuilder:
    @staticmethod
    def _get_adjust(rows: list[list[T]], adjust: int) -> list[list[T]]:
        buttons: list[T] = []

        for button_row in rows:
            for button in button_row:
                buttons.append(button)

        rows_len = len(buttons)

        result: list[list[T]] = []
        row: list[T] = []

        for index in range(0, rows_len):
            row.append(buttons[index])

            if (index + 1) % adjust == 0:
                result.append(row.copy())

                row.clear()

        if row:
            result.append(row.copy())

        return result

    @staticmethod
    def _get_inline_keyboard(
            rows: tuple[Row, ...],
            adjust: Optional[int]
    ) -> list[list[InlineKeyboardButton]]:

        rows_list = []

        for row in rows:
            rows_list.append(row.get_rows())

        return BaseBuilder._get_different_keyboar(rows_list, adjust)

    @staticmethod
    def _get_reply_keyboard(
            rows: tuple[ReplyRow, ...],
            adjust: Optional[int]
    ) -> list[list[KeyboardButton]]:

        rows_list = []

        for row in rows:
            rows_list.append(row.get_rows())

        return BaseBuilder._get_different_keyboar(rows_list, adjust)

    @staticmethod
    def _get_different_keyboar(
            rows: list[list[T]],
            adjust: Optional[int]
    ) -> list[list[T]]:
        if not rows:
            return []

        if adjust is None or adjust < 0:
            return rows

        return BaseBuilder._get_adjust(rows, adjust)

    @staticmethod
    def ignore_params(*args) -> tuple[Any, ...]:
        return args


class Builder(BaseBuilder, InlineKeyboardMarkup):
    def __new__(
            cls,
            *rows: Row,
            adjust: Optional[int] = None,
    ):
        keyboard = cls._get_inline_keyboard(rows, adjust)

        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    def __init__(self, *rows: Row, adjust: Optional[int] = None):
        # This code is never get and made for Pydantic plugin
        super().__init__(inline_keyboard=[])

        self.ignore_params(rows, adjust)


class ReplyBuilder(BaseBuilder, ReplyKeyboardMarkup):
    def __new__(
            cls,
            *rows: ReplyRow,
            adjust: Optional[int] = None,
            resize_keayboard: Optional[bool] = None,
            is_persistent: Optional[bool] = None,
            one_time_keyboard: Optional[bool] = None,
    ):
        keyboard = cls._get_reply_keyboard(rows, adjust)

        return ReplyKeyboardMarkup(
            keyboard=keyboard,
            resize_keyboard=resize_keayboard,
            is_persistent=is_persistent,
            one_time_keyboard=one_time_keyboard
        )

    def __init__(
            self,
            *rows: ReplyRow,
            adjust: Optional[int] = None,
            resize_keayboard: Optional[bool] = None,
            is_persistent: Optional[bool] = None,
            one_time_keyboard: Optional[bool] = None,
    ):
        # This code is never get and made for Pydantic plugin

        super().__init__(keyboard=[])

        self.ignore_params(
            rows,
            adjust,
            resize_keayboard,
            is_persistent,
            one_time_keyboard
        )
