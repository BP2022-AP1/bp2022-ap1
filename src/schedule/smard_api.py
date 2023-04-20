from dataclasses import dataclass
from datetime import datetime

import marshmallow as marsh
import pytz
import requests
from peewee import DateTimeField, FloatField, ForeignKeyField

from src.base_model import BaseModel


class SmardApiIndex(BaseModel):
    class Schema(BaseModel.Schema):
        timestamp = marsh.fields.DateTime(required=True)

        def _make(self, data: dict) -> "SmardApiIndex":
            """Constructs a SmardApiIndex from a dict

            :param data: The dict
            :return: A SmardApiIndex
            """
            return SmardApiIndex(**data)

    timestamp = DateTimeField(unique=True)


class SmardApiEntry(BaseModel):
    class Schema(BaseModel.Schema):
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
    @classmethod
    def none(cls):
        return cls(False, False, None, None)

    available: bool
    interval_altered: bool
    start: datetime
    end: datetime


class SmardApi:
    RESOLUTION: str = "quarterhour"
    FILTER: str = "1223"  # Braunkohle
    REGION: str = "50Hertz"  # name of the electricity grid company in eastern Germany
    BASE_URL: str = f"https://www.smard.de/app/chart_data/{FILTER}/{REGION}"

    _timezone: str

    def __init__(self, timezone: str = "Europe/Berlin"):
        self._timezone = timezone
        self._update_indices()

    def timestamp_to_dt(self, timestamp: int) -> datetime:
        return datetime.fromtimestamp(
            timestamp / 1000, tz=pytz.timezone(self._timezone)
        )

    def _request(self, url: str) -> dict:
        response = requests.get(url, headers={"Accept": "application/json"})
        return response.json()

    def _request_data(self, index: SmardApiIndex) -> dict:
        url = (
            f"{self.BASE_URL}/{self.FILTER}_{self.REGION}"
            f"_{self.RESOLUTION}_{index.timestamp}.json"
        )
        for timestamp, value in self._request(url)["series"]:
            SmardApiEntry.get_or_create(
                timestamp=self.timestamp_to_dt(timestamp), value=value, index_id=index
            )

    def _update_indices(self):
        url = f"{self.BASE_URL}/index_{self.RESOLUTION}.json"
        index_timestamps = self._request(url)["timestamps"]
        for index_timestamp in index_timestamps:
            SmardApiIndex.get_or_create(timestamp=self.timestamp_to_dt(index_timestamp))

    def _start_index_from_timestamp(
        self, start: datetime, end: datetime
    ) -> tuple[SmardApiIndex | None, bool]:
        try:
            return (
                SmardApiIndex.select()
                .where(SmardApiIndex.timestamp <= start)
                .order_by(SmardApiIndex.timestamp.desc())
                .first()
            ), False
        except SmardApiIndex.DoesNotExist:
            start_index = (
                SmardApiIndex.select().order_by(SmardApiIndex.timestamp.asc()).first()
            )
            if start_index.timestamp > end:
                return None, True
            return start_index, True

    def _end_index_from_timestamp(
        self, start: datetime, end: datetime
    ) -> tuple[SmardApiIndex | None, bool]:
        try:
            return (
                SmardApiIndex.select()
                .where(SmardApiIndex.timestamp >= end)
                .order_by(SmardApiIndex.timestamp.asc())
                .first()
            ), False
        except SmardApiIndex.DoesNotExist:
            end_index = (
                SmardApiIndex.select().order_by(SmardApiIndex.timestamp.desc()).first()
            )
            if end_index.timestamp < start:
                return None, True
            return end_index, True

    def _request_indices_between(
        self, start_index: SmardApiIndex, end_index: SmardApiIndex
    ):
        indices = SmardApiIndex.select().where(
            SmardApiIndex.timestamp >= start_index.timestamp,
            SmardApiIndex.timestamp <= end_index.timestamp,
        )
        for index in indices:
            if len(index.entries) == 0:
                self._request_data(index)

    def _get_data(self, start: datetime, end: datetime) -> list[SmardApiEntry]:
        return (
            SmardApiEntry.select()
            .where(SmardApiEntry.timestamp >= start, SmardApiEntry.timestamp <= end)
            .order_by(SmardApiEntry.timestamp.asc())
        )

    def data_availability(
        self, start: datetime, end: datetime
    ) -> SmardDataAvailability:
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
        availability = self.data_availability(start, end)
        if not availability.available:
            return []
        return self._get_data(availability.start, availability.end)
