

import sys

from typing import Any

from enum import Enum
from decimal import Decimal

from datetime import date, time, datetime

from pydantic import BaseModel

from usefulgram.exceptions import TooMoreCharacters
from usefulgram.enums import Const


class _Additional:
    @staticmethod
    def _add_separator(item: str, separator: str = "&") -> str:
        return f"{item}{separator}"

    def _object_to_str(self, item: object) -> str:
        if isinstance(item, BaseModel):
            fields = item.model_fields

        else:
            fields = item.__annotations__

        annotations_keys = list(fields.keys())

        result = ""

        for key in annotations_keys:
            if key == "prefix":
                continue

            values = item.__getattribute__(f"{key}")

            string_value = self._to_str(values, is_recursion=True)

            result += self._add_separator(string_value)

        return result[:-1]

    def _to_str(self, item: Any, is_recursion: bool = False) -> str:
        if item is None:
            return ""

        if isinstance(item, bool):
            return str(int(item))

        if isinstance(item, str):
            return item

        if isinstance(item, (int, float, Decimal)):
            return str(item)

        if isinstance(item, (datetime, date, time)):
            return item.strftime(Const.DATETIME_FORMAT)

        if isinstance(item, Enum):
            return item.name

        if is_recursion:
            return self._object_to_str(item)

        try:
            return self._object_to_str(item)

        except AttributeError:
            return f"{item}"

    def __call__(self, *args: Any) -> str:
        if args == ():
            return ""

        result = ""

        for item in args:
            result += self._add_separator(self._to_str(item))

        result = result[:-1]

        return result


class _CallbackData:
    @staticmethod
    def _get_str_callback_data(
            prefix: str, additional: str, separator: str
    ) -> str:

        return f"{prefix}{separator}{additional}"

    @staticmethod
    def _check_callback_data_bytes(callback_data: str) -> bool:
        size = sys.getsizeof(callback_data)

        true_size = size - 37  # 37 - is a system empty string lenght

        if true_size < 64:
            return True

        raise TooMoreCharacters

    def __call__(
            self, prefix: str,
            *args: Any,
            separator: str = "/") -> str:

        additional = AdditionalInstance(*args)

        callback_data = self._get_str_callback_data(
            prefix, additional, separator
        )

        self._check_callback_data_bytes(callback_data)

        return callback_data


AdditionalInstance = _Additional()
CallbackData = _CallbackData()
