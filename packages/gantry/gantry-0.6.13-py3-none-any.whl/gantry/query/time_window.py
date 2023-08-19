import datetime
from typing import Optional, Union


class TimeWindow:
    def __init__(
        self, start_time: Union[str, datetime.datetime], end_time: Union[str, datetime.datetime]
    ):
        """
        Initialize a standard time window.

        Args:
            start_time (Union[str, datetime.datetime]): the start time of the time window.
            end_time (Union[str, datetime.datetime]): the end time of the time window.
        """
        self.start_time = start_time
        self.end_time = end_time


class RelativeTimeWindow(TimeWindow):
    def __init__(
        self,
        window_length: datetime.timedelta,
        offset: Optional[datetime.timedelta] = None,
    ):
        """
        Initialize a relative time window.

        Args:
            window_length (datetime.timedelta): the length of the time window.
            offset (Optional[datetime.timedelta]): the offset of the time window. Defaults to None.
        """
        self.window_length = window_length
        self.offset = offset or datetime.timedelta()
        end_time: datetime.datetime = (
            datetime.datetime.utcnow() - self.offset if self.offset else datetime.datetime.utcnow()
        )
        start_time: datetime.datetime = end_time - window_length
        super().__init__(start_time, end_time)
