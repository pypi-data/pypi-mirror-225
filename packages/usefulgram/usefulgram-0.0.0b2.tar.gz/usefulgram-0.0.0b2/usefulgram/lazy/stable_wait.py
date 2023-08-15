

from datetime import datetime, timedelta, timezone

from usefulgram.enums.const import Const


class StableWaiter:
    @staticmethod
    def _get_delta_between_current_and_datetime(
            message_datetime: datetime
    ) -> timedelta:

        current = datetime.now(tz=timezone.utc)

        return current - message_datetime

    @staticmethod
    def get_stable_wait_time(dt: datetime) -> float:
        delta = StableWaiter._get_delta_between_current_and_datetime(dt)

        total_seconds = delta.total_seconds()

        if total_seconds < 0:
            total_seconds = 0

        wait_time = Const.STABLE_WAIT_TIME_SECONDS - total_seconds

        return round(wait_time, 3)
