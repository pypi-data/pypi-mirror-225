

from typing import Optional, Union
from datetime import date

from usefulgram.enums.calendar import CalendarEnum
from usefulgram.filters.parse_filters import BasePydanticFilter


class CalendarChangeButton(BasePydanticFilter):
    prefix: str = "calendar_change"
    year: Optional[int] = None
    month: Optional[int] = None


class CalendarInfoButton(BasePydanticFilter):
    prefix: str = "calendar_info"
    button_type: Union[CalendarEnum, str, None] = None


class CalendarDateFilter(BasePydanticFilter):
    date_value: Optional[date] = None
