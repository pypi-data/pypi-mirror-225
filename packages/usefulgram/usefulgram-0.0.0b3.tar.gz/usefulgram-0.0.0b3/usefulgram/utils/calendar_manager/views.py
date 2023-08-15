

import calendar as python_calendar
from typing import Optional, Iterable, Coroutine, Any, Union
from datetime import datetime, date

from aiogram.types import InlineKeyboardMarkup, Message

from usefulgram.enums.calendar import CalendarEnum
from usefulgram.lazy import LazySender, LazyEditor
from usefulgram.keyboard import Builder, Row, Button
from usefulgram.utils.calendar_manager.filters import (
    CalendarChangeButton,
    CalendarInfoButton,
    CalendarDateFilter
)

from usefulgram.utils.calendar_manager.model import BaseCalendar, en_calendar


class Calendar:
    @staticmethod
    def _get_minus_month_and_year(month: int, year: int) -> tuple[int, int]:
        if month - 1 < 1:
            return 12, year - 1

        return month - 1, year

    @staticmethod
    def _get_plus_month_and_year(month: int, year: int) -> tuple[int, int]:
        if month + 1 > 12:
            return 1, year + 1

        return month + 1, year

    @staticmethod
    def _get_change_month_button(
            month: int,
            year: int,
            is_right: bool
    ) -> Button:

        if is_right:
            text = "⇨"

        else:
            text = "⇦"

        return Button(text, CalendarChangeButton(year=year, month=month))

    @staticmethod
    def _get_heading(weekdays: Iterable[str]) -> Row:
        heading_buttons = []

        for day in weekdays:
            heading_buttons.append(
                Button(
                    day, CalendarInfoButton(button_type=CalendarEnum.WEEKDAY))
            )

        return Row(*heading_buttons)

    @staticmethod
    def _get_format_date(month: int, year: int) -> str:
        return f"{month}.{year}"

    def _get_format_date_button(self, month: int, year: int) -> Button:
        text = self._get_format_date(month, year)

        return Button(text, CalendarInfoButton(button_type=CalendarEnum.DATE))

    @staticmethod
    def _get_current_date() -> date:
        return datetime.now().date()

    @staticmethod
    def _get_calendar(year: int, month: int) -> Iterable[date]:
        return python_calendar.Calendar().itermonthdates(year, month)

    @staticmethod
    def _get_calendars_day_buttons(
            days: Iterable[date],
            current_date: date,
            month: int,
            result_class: CalendarDateFilter
    ) -> list[Row]:

        row_list: list[Row] = []
        current_row: list[Button] = []

        for index, day in enumerate(days):
            if index % 7 == 0:
                row_list.append(Row(*current_row))
                current_row = []

            if day.month != month:
                current_row.append(
                    Button(
                        " ",
                        CalendarInfoButton(button_type=CalendarEnum.EMPTY))
                )

                continue

            if day == current_date:
                humanize_day = f"[{day.day}]"

            else:
                humanize_day = str(day.day)

            result_class.date_value = day

            current_row.append(
                Button(humanize_day, result_class)
            )

        row_list.append(Row(*current_row))

        return row_list

    def _get_days_buttons(
            self,
            month: int,
            year: int,
            result_class: CalendarDateFilter
    ) -> list[Row]:

        current_date = self._get_current_date()

        month_day = self._get_calendar(year, month)

        return self._get_calendars_day_buttons(
            days=month_day,
            current_date=current_date,
            month=month,
            result_class=result_class
        )

    def _get_bottom_buttons(self, month: int, year: int) -> Row:
        left_month, left_year = self._get_minus_month_and_year(month, year)
        right_month, right_year = self._get_plus_month_and_year(month, year)

        left_button = self._get_change_month_button(
            left_month, left_year, is_right=False
        )
        right_button = self._get_change_month_button(
            right_month, right_year, is_right=True
        )

        date_button = self._get_format_date_button(month, year)

        return Row(left_button, date_button, right_button)

    @staticmethod
    def _get_calendar_markup(
            heading: Row, day_buttons: list[Row], bottom_buttons: Row
    ) -> InlineKeyboardMarkup:

        return Builder(
            heading,
            *day_buttons,
            bottom_buttons
        )

    def show(
            self,
            sender: LazySender,
            month: int,
            year: int,
            result_class: CalendarDateFilter,
            text: Optional[str] = None,
            localization_class: BaseCalendar = en_calendar,
            editor: Optional[LazyEditor] = None
    ) -> Coroutine[Any, Any, Union[Message, bool]]:
        """
        Send or edit the calendar
        :param text:
        :param sender:
        :param month:
        :param year:
        :param result_class:
        :param localization_class:
        :param editor:
        :return:
        """

        heading = self._get_heading(localization_class.weekdays)
        day_buttons = self._get_days_buttons(month, year, result_class)
        bottom_buttons = self._get_bottom_buttons(month, year)

        markup = self._get_calendar_markup(
            heading, day_buttons, bottom_buttons
        )

        if editor is not None:
            return editor.edit(text=text, reply_markup=markup)

        return sender.send(text=text, reply_markup=markup)


calendar_manager = Calendar()
