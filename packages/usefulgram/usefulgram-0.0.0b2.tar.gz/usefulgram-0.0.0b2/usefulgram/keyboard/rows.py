

from aiogram.types import (
    InlineKeyboardButton,
    KeyboardButton,
)


class Row:
    rows: list[InlineKeyboardButton]

    def __init__(self, *args: InlineKeyboardButton):
        self.rows = [*args]

    def get_rows(self) -> list[InlineKeyboardButton]:
        return self.rows


class ReplyRow:
    rows: list[KeyboardButton]

    def __init__(self, *args: KeyboardButton):
        self.rows = [*args]

    def get_rows(self) -> list[KeyboardButton]:
        return self.rows
