from dataclasses import dataclass
from datetime import datetime

import marshmallow as marsh
import pytz
import requests
from peewee import DateTimeField, FloatField, ForeignKeyField, DoesNotExist

from src.base_model import BaseModel


class SmardApiIndex(BaseModel):
    """This class models an index timestamp of the smard api. Each data
    entry is linked to an index timestamp. This is due to the API desgin.
    The Smard API can only deliver batches of data. The time intervals of
    these batches are fixed (The API works more like a ftp server). The first
    timestamp of such a batch is its index timestamp. You need the index timestamp
    to request the data of the batch.
    """

    class Schema(BaseModel.Schema):
        """marshmallow schema for SmardApiIndex"""

        timestamp = marsh.fields.DateTime(required=True)

        def _make(self, data: dict) -> "SmardApiIndex":
            """Constructs a SmardApiIndex from a dict

            :param data: The dict
            :return: A SmardApiIndex
            """
            return SmardApiIndex(**data)

    timestamp = DateTimeField(unique=True)


class SmardApiEntry(BaseModel):
    """This class models an entry of the smard api. Each entry is linked to an
    index timestamp. It contains the timestamp and the value of the entry.
    The value is the amount of electricity produced from coal in
    a quarter hour in megawatt hours.
    """

    class Schema(BaseModel.Schema):
        """marshmallow schema for SmardApiEntry"""

        timestamp = marsh.fields.DateTime(required=True)
        value = marsh.fields.Float(required=True)

        def _make(self, data: dict) -> "SmardApiEntry":
            """Constructs a SmardApiEntry from a dict

            :param data: The dict
            :return: A SmardApiEntry
            """
            return SmardApiEntry(**data)

    timestamp = DateTimeField(unique=True)
    value = FloatField(null=True)
    index_id = ForeignKeyField(SmardApiIndex, backref="entries")


@dataclass
class SmardDataAvailability:
    """This class represents the availability of data from the smard api.
    It is the return type of SmardApi.data_availability. If available is
    True there is data available for the given time interval. If interval_altered
    is True the time interval was altered because only a subset of the requested
    interval contained data. The start and end attributes contain the actual
    time interval for which data is available. They can be slitely different
    from the requested time interval even if interval_altered is False to
    match the exact time intervals of the data batches.
    """

    @classmethod
    def none(cls):
        """Returns a SmardDataAvailability object that represents the
        case that no data is available.

        :return: A SmardDataAvailability object
        """
        return cls(False, False, None, None)

    available: bool
    interval_altered: bool
    start: datetime
    end: datetime


class SmardApi:
    """This class provides an interface to the smard api. It provides
    quarter hourly data of the amount of electricity produced from coal.
    """

    RESOLUTION: str = "quarterhour"
    FILTER: str = "1223"  # Braunkohle
    REGION: str = "50Hertz"  # name of the electricity grid company in eastern Germany
    BASE_URL: str = f"https://www.smard.de/app/chart_data/{FILTER}/{REGION}"

    _timezone: str

    def __init__(self, timezone: str = "Europe/Berlin"):
        """Constructs a SmardApi

        :param timezone: The timezone to use for the timestamps
        """
        self._timezone = timezone
        self._update_indices()

    def timestamp_to_dt(self, timestamp: int) -> datetime:
        """Converts a timestamp to a datetime object

        :param timestamp: The timestamp
        :return: The datetime object
        """
        return datetime.fromtimestamp(
            timestamp / 1000, tz=pytz.timezone(self._timezone)
        )

    def _request(self, url: str) -> dict:
        """Sends a get request to the given url and returns the response as a dict

        :param url: The url
        :return: The response as a dict
        """
        response = requests.get(
            url,
            timeout=10,
            headers={"Accept": "application/json"}
        )
        return response.json()

    def _request_data(self, index: SmardApiIndex):
        """Requests the data of the given index timestamp and
        writes it to the database

        :param index: The index timestamp
        """
        url = (
            f"{self.BASE_URL}/{self.FILTER}_{self.REGION}"
            f"_{self.RESOLUTION}_{index.timestamp}.json"
        )
        for timestamp, value in self._request(url)["series"]:
            SmardApiEntry.get_or_create(
                timestamp=self.timestamp_to_dt(timestamp), value=value, index_id=index
            )

    def _update_indices(self):
        """Updates the database with the index timestamps of the smard api"""
        url = f"{self.BASE_URL}/index_{self.RESOLUTION}.json"
        index_timestamps = self._request(url)["timestamps"]
        for index_timestamp in index_timestamps:
            SmardApiIndex.get_or_create(timestamp=self.timestamp_to_dt(index_timestamp))

    def _start_index_from_timestamp(
        self, start: datetime, end: datetime
    ) -> tuple[SmardApiIndex | None, bool]:
        """Returns the index timestamp that is closest to the given start timestamp
        and a boolean that indicates if the start timestamp was altered

        :param start: The start timestamp
        :param end: The end timestamp
        :return: The index timestamp and the boolean
        """
        try:
            return (
                SmardApiIndex.select()
                .where(SmardApiIndex.timestamp <= start)
                .order_by(SmardApiIndex.timestamp.desc())
                .first()
            ), False
        except DoesNotExist:
            start_index = (
                SmardApiIndex.select().order_by(SmardApiIndex.timestamp.asc()).first()
            )
            if start_index.timestamp > end:
                return None, True
            return start_index, True

    def _end_index_from_timestamp(
        self, start: datetime, end: datetime
    ) -> tuple[SmardApiIndex | None, bool]:
        """Returns the index timestamp that is closest to the given end timestamp
        and a boolean that indicates if the end timestamp was altered

        :param start: The start timestamp
        :param end: The end timestamp
        :return: The index timestamp and the boolean
        """
        try:
            return (
                SmardApiIndex.select()
                .where(SmardApiIndex.timestamp >= end)
                .order_by(SmardApiIndex.timestamp.asc())
                .first()
            ), False
        except DoesNotExist:
            end_index = (
                SmardApiIndex.select().order_by(SmardApiIndex.timestamp.desc()).first()
            )
            if end_index.timestamp < start:
                return None, True
            return end_index, True

    def _is_last_index(self, index: SmardApiIndex) -> bool:
        """Returns True if the given index is the last index timestamp

        :param index: The index timestamp
        :return: True if the given index is the last index timestamp
        """
        return (
            index
            == SmardApiIndex.select().order_by(SmardApiIndex.timestamp.desc()).first()
        )

    def _request_indices_between(
        self, start_index: SmardApiIndex, end_index: SmardApiIndex
    ):
        """Requests the data of all indices between the given start and end index

        :param start_index: The start index timestamp
        :param end_index: The end index timestamp
        """
        indices = SmardApiIndex.select().where(
            SmardApiIndex.timestamp >= start_index.timestamp,
            SmardApiIndex.timestamp <= end_index.timestamp,
        )
        # I don't now why the linter complains here
        # pylint: disable=not-an-iterable
        for index in indices:
            if len(index.entries) == 0 or self._is_last_index(index):
                self._request_data(index)

    def _get_data(self, start: datetime, end: datetime) -> list[SmardApiEntry]:
        """Returns the data between the given start and end timestamp

        :param start: The start timestamp
        :param end: The end timestamp
        :return: The data between the given start and end timestamp
        """
        return (
            SmardApiEntry.select()
            .where(SmardApiEntry.timestamp >= start, SmardApiEntry.timestamp <= end)
            .order_by(SmardApiEntry.timestamp.asc())
        )

    def data_availability(
        self, start: datetime, end: datetime
    ) -> SmardDataAvailability:
        """Returns the data availability between the given start and end timestamp

        :param start: The start timestamp
        :param end: The end timestamp
        :return: The data availability between the given start and end timestamp
        """
        if start > end:
            return SmardDataAvailability.none()

        start_index, altered_interval = self._start_index_from_timestamp(start, end)
        if start_index is None:
            return SmardDataAvailability.none()
        end_index, altered_interval = self._end_index_from_timestamp(start, end)
        if end_index is None:
            return SmardDataAvailability.none()
        self._request_indices_between(start_index, end_index)

        data = self._get_data(start, end)

        found_start = next(
            (entry.timestamp for entry in data if entry.value is not None), None
        )
        found_end = next(
            (entry.timestamp for entry in reversed(data) if entry.value is not None),
            None,
        )
        if found_start is None or found_end is None:
            return SmardDataAvailability.none()
        altered_interval = (
            found_start != data[0].timestamp or found_end != data[-1].timestamp
        )
        return SmardDataAvailability(True, altered_interval, found_start, found_end)

    def get_data(self, start: datetime, end: datetime) -> list[SmardApiEntry]:
        """Returns the data between the given start and end timestamp

        :param start: The start timestamp
        :param end: The end timestamp
        :return: The data between the given start and end timestamp
        """
        availability = self.data_availability(start, end)
        if not availability.available:
            return []
        return self._get_data(availability.start, availability.end)
