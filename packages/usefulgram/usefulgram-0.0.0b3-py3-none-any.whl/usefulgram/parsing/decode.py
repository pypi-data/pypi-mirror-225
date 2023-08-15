

from typing import Union, Any, Optional, Type
from datetime import datetime, date, time

from usefulgram.enums import Const
from usefulgram.exceptions import WrongObjectType

from enum import Enum

from pydantic import BaseModel

from contextlib import suppress


class DecodeCallbackData:
    prefix: str
    additional: list[str]

    @staticmethod
    def _get_prefix_and_additional(
            callback_data: str,
            separator: str
    ) -> tuple[str, list[str]]:

        split_data = callback_data.split(separator)

        additional = split_data[1].split("&")

        return split_data[0], additional

    @staticmethod
    def _get_empty_prefix_and_additional() -> tuple[str, list[str]]:
        return "", []

    def __init__(self, callback_data: Optional[str], separator: str = "/"):
        if callback_data is not None:
            self.prefix, self.additional = self._get_prefix_and_additional(
                callback_data, separator
            )

            return

        self.prefix, self.additional = self._get_empty_prefix_and_additional()

    def _convert_typing_object_to_type(
            self, obj_value: str, *args: type
    ) -> Any:

        for obj_type in args:
            with suppress(ValueError, TypeError):
                return self._convert_str_to_type(
                    obj_value=obj_value,
                    obj_type=obj_type
                )

        raise WrongObjectType

    def _convert_str_to_type(
            self,
            obj_value: str,
            obj_type: Any
    ) -> Any:

        if obj_value == "":
            return None

        # Optional[...] or Union[...] checker
        if not isinstance(obj_type, type):
            irregular_types = obj_type.__getattribute__("__args__")

            return self._convert_typing_object_to_type(
                obj_value, *irregular_types
            )

        if issubclass(obj_type, bool):
            return bool(int(obj_value))

        if issubclass(obj_type, datetime):
            return datetime.strptime(obj_value, Const.DATETIME_FORMAT)

        if issubclass(obj_type, date):
            return datetime.strptime(obj_value, Const.DATETIME_FORMAT).date()

        if issubclass(obj_type, time):
            return datetime.strptime(obj_value, Const.DATETIME_FORMAT).time()

        if issubclass(obj_type, Enum):
            return obj_type[obj_value]

        try:
            return obj_type(obj_value)  # type: ignore

        except (ValueError, AttributeError):
            raise WrongObjectType

    @staticmethod
    def _is_dataclass(obj_type: Any) -> bool:
        if isinstance(obj_type, type):
            return issubclass(obj_type, BaseModel)

        try:
            irregular_types = obj_type.__getattribute__("__args__")

        except (ValueError, AttributeError):
            return False

        for irregular_type in irregular_types:
            if issubclass(irregular_type, BaseModel):
                return True

        return False

    @staticmethod
    def _get_dataclass_obj(obj_type: Any) -> Type[BaseModel]:
        if isinstance(obj_type, type):
            if issubclass(obj_type, BaseModel):
                return obj_type

        irregular_types = obj_type.__getattribute__("__args__")

        for irregular_type in irregular_types:
            if issubclass(irregular_type, BaseModel):
                return irregular_type

        raise WrongObjectType

    def _iter_key_and_type(
            self, keys: list[str], objects_types: list[type],
            add_prefix: bool, start_additional_value: int = 0
    ) -> dict[str, Any]:

        return_param: dict[str, Any] = {}

        if add_prefix:
            return_param["prefix"] = self.prefix

        additional_value = start_additional_value

        for key, obj_type in zip(keys, objects_types):

            if key == "prefix":
                return_param[key] = self._convert_str_to_type(
                    self.prefix, obj_type
                )

                continue

            if self._is_dataclass(obj_type):
                dataclass_obj = self._get_dataclass_obj(obj_type)

                keys, values = self._get_key_and_values_by_obj(
                    format_object=dataclass_obj
                )

                params = self._iter_key_and_type(
                    keys=keys,
                    objects_types=values,
                    add_prefix=False,
                    start_additional_value=additional_value
                )

                additional_value += len(keys)

                return_param[key] = self._get_convert_obj(dataclass_obj, params)

                continue

            return_param[key] = self._convert_str_to_type(
                self.additional[additional_value], obj_type
            )

            additional_value += 1

        return return_param

    @staticmethod
    def _get_convert_obj(
            format_obj: type, params: dict[str, Any]
    ) -> Union[BaseModel, object]:
        return format_obj(**params)

    @staticmethod
    def _get_key_and_values_by_obj(
            format_object: type
    ) -> tuple[list[str], list[Any]]:

        if issubclass(format_object, BaseModel):
            fields = format_object.model_fields
            values = [i.annotation for i in fields.values()]

            return list(fields.keys()), values

        fields = format_object.__annotations__

        another_values = list(fields.values())

        return list(fields.keys()), another_values

    def to_format(
            self, format_object: type, add_prefix: bool = False
    ) -> Union[BaseModel, object]:

        keys, values = self._get_key_and_values_by_obj(format_object=format_object)

        obj_params = self._iter_key_and_type(keys, values, add_prefix)

        return self._get_convert_obj(format_object, obj_params)

    @staticmethod
    def class_to_dict(class_: Union[BaseModel, object]) -> dict[str, Any]:
        result_dict = {"prefix": class_.__getattribute__("prefix")}

        if isinstance(class_, BaseModel):
            fields = class_.model_fields

        else:
            fields = class_.__annotations__

        for key in fields.keys():
            result_dict[key] = class_.__getattribute__(key)

        return result_dict
