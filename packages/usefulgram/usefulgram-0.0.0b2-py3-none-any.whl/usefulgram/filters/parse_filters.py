

from typing import Optional, Union, Dict, Any, Tuple, Iterable
from abc import ABC, abstractmethod

from pydantic import BaseModel

from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery

from aiogram.filters.magic_data import MagicData
from aiogram.utils.magic_filter import MagicFilter

from usefulgram.parsing.decode import DecodeCallbackData
from usefulgram.exceptions import UndefinedMagicFilterModel


class _BaseMagicFilter(ABC):
    _magic_filter: Optional[tuple[MagicFilter]] = None

    def filter(self, *args: MagicFilter):
        self.__setattr__("_magic_filter", args)

        return self

    @staticmethod
    async def _ckeck_magic_filter(
            callback: CallbackQuery,
            magic_filter: tuple[MagicFilter],
            values: Optional[tuple[Any, ...]] = None,
            model: Optional[dict[Any, Any]] = None
    ) -> bool:

        for filter_obj in magic_filter:
            filter_instance = MagicData(filter_obj)

            if values is not None:
                result = await filter_instance(callback, *values)

            elif model is not None:
                result = await filter_instance(callback, **model)

            else:
                raise UndefinedMagicFilterModel

            if not result:
                return False

        return True

    def get_magic_filter(self) -> Any:
        try:
            return self.__getattribute__("_magic_filter")

        except AttributeError:
            return None


class _BaseDataclassesFilter(_BaseMagicFilter, ABC):
    @abstractmethod
    async def __call__(self, callback: CallbackQuery, decoder: DecodeCallbackData):
        """
        This abstract method should use the get_filter method
        :param callback:
        :param decoder:
        :return:
        """
        pass

    async def get_filter(
            self,
            callback: CallbackQuery,
            decoder: DecodeCallbackData,
            fields_name: Iterable[str]
    ) -> Union[bool, Dict[str, Any]]:

        try:
            callback_data_model = decoder.to_format(type(self), add_prefix=True)

        except (AttributeError, ValueError, IndexError, KeyError):
            return False

        for item_name in fields_name:
            if item_name == "_magic_filter":
                continue

            filter_value = self.__getattribute__(item_name)

            if filter_value is None:
                continue

            data_value = callback_data_model.__getattribute__(item_name)

            if data_value != filter_value:
                return False

        magic_filter: Optional[tuple[MagicFilter]] = super().get_magic_filter()

        if magic_filter is not None:
            if await self._ckeck_magic_filter(
                callback=callback,
                magic_filter=magic_filter,
                model=decoder.class_to_dict(callback_data_model)
            ):
                return decoder.class_to_dict(callback_data_model)

            return False

        return decoder.class_to_dict(callback_data_model)


class BasePydanticFilter(_BaseDataclassesFilter, BaseModel, BaseFilter):
    prefix: Optional[str] = None

    async def __call__(
            self,
            callback: CallbackQuery,
            decoder: DecodeCallbackData
    ) -> Union[bool, Dict[str, Any]]:

        fields = self.model_fields.keys()

        return await self.get_filter(
            callback=callback,
            decoder=decoder,
            fields_name=fields
        )


class CallbackPrefixFilter(BaseFilter):
    def __init__(self, prefix: str):
        """

        :param prefix: first argument in callback data
        """
        self.prefix = prefix

    async def __call__(self, message: CallbackQuery,
                       decoder: DecodeCallbackData) -> bool:

        if self.prefix == decoder.prefix:
            return True

        return False


class ItarationFilter(_BaseMagicFilter):
    def __init__(self, item_number: int = 0):
        self._item_number: int = item_number
        self._operation: Optional[Tuple[str, Any]] = None
        self._error_result: bool = False

    def __getitem__(self, item: int):
        self._item_number = item

        return self

    @staticmethod
    def _convert(other: str) -> Optional[int]:
        try:
            return int(other)

        except ValueError:
            return None

    def __eq__(self, other: Any):
        self._operation = ("eq", other)

        return self

    def __ne__(self, other: Any):
        self._operation = ("ne", other)

        return self

    def __lt__(self, other: Any):
        self._operation = ("lt", other)

        return self

    def __gt__(self, other: Any):
        self._operation = ("gt", other)

        return self

    def __le__(self, other: Any):
        self._operation = ("le", other)

        return self

    def __ge__(self, other: Any):
        self._operation = ("ge", other)

        return self

    @staticmethod
    def _do_operation(operation: str, first_item: Any, second_item: Any):
        if operation == "eq":
            return first_item == second_item

        if operation == "ne":
            return first_item != second_item

        first_item = ItarationFilter._convert(first_item)

        if first_item is False:
            return False

        if operation == "lt":
            return first_item < second_item

        if operation == "gt":
            return first_item > second_item

        if operation == "le":
            return first_item <= second_item

        if operation == "ge":
            return first_item >= second_item

    async def __call__(
            self, callback: CallbackQuery,
            decoder: DecodeCallbackData
    ):

        magic_filter: Optional[tuple[MagicFilter]] = super().get_magic_filter()

        if self._error_result:
            return False

        values = (decoder.prefix, *decoder.additional)

        first_item = values[self._item_number]

        if magic_filter is not None:
            if await self._ckeck_magic_filter(
                    callback=callback,
                    magic_filter=magic_filter,
                    values=values
            ):
                return True

            return False

        if self._operation is None:
            return False

        operation, second_item = self._operation

        return self._do_operation(operation, first_item, second_item)
