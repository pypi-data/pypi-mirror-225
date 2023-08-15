

from pydantic import BaseModel


# this.. temporary solution

class BaseCalendar(BaseModel):
    weekdays: tuple[str, str, str, str, str, str, str]


en_calendar = BaseCalendar(
    weekdays=(
        "Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"
    )
)

ru_calendar = BaseCalendar(
    weekdays=(
        "Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"
    )
)
