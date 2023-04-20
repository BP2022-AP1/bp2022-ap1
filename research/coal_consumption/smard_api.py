from datetime import datetime

import matplotlib.pyplot as plt
import pytz
import requests


class DataProvider:
    """This class can load data from the smard API in a more convinient
    way then using the raw API. It also caches data to circumvent
    rate limiting.
    """

    @staticmethod
    def timestamp_to_dt(timestamp: int) -> datetime:
        """Convert smard timestamp to datatime object

        :param timestamp: The smard timestamp (Unix timestamp * 1000)
        :return: A datetime object
        """
        return datetime.fromtimestamp(
            timestamp / 1000, tz=pytz.timezone("Europe/Berlin")
        )

    RESOLUTION: str = "quarterhour"
    FILTER: str = "1223"  # Braunkohle
    REGION: str = "50Hertz"
    BASE_URL: str = f"https://www.smard.de/app/chart_data/{FILTER}/{REGION}"

    _available_index_timestamps: list[int]
    _loaded_data: list[tuple[datetime, float]]
    _loaded_data_index_timestamps: set[int]

    def __init__(self):
        """Initializer for DataProvider"""
        self._available_index_timestamps = []
        self._loaded_data = []
        self._loaded_data_index_timestamps = set()
        self._load_index_timestamps()

    def _load_index_timestamps(self) -> list[int]:
        """Loads all index timestamps from the API"""
        url = f"{self.BASE_URL}/index_{self.RESOLUTION}.json"
        response = requests.get(url, headers={"Accept": "application/json"})
        self._available_index_timestamps = response.json()["timestamps"][1:]

    def _load_data(self, index_timestamp: int):
        """Loads data in the file referenced by index_timestamp from
        the API and caches it.
        """
        url = f"{self.BASE_URL}/{self.FILTER}_{self.REGION}_{self.RESOLUTION}_{index_timestamp}.json"
        response = requests.get(url, headers={"Accept": "application/json"})
        result = response.json()["series"]

        if index_timestamp != self._available_index_timestamps[-1]:
            self._loaded_data_index_timestamps.add(index_timestamp)

        for timestamp, value in result:
            self._loaded_data.append((self.timestamp_to_dt(timestamp), value))

        self._loaded_data.sort(key=lambda x: x[0])

    def _start_index(self, start: datetime) -> int:
        """Computes the index into the _available_index_timestamps where start lies in"""
        return max(
            self._available_index_timestamps.index(
                [
                    timestamp
                    for timestamp in self._available_index_timestamps
                    if start <= self.timestamp_to_dt(timestamp)
                ][0]
            )
            - 1,
            0,
        )

    def _end_index(self, end: datetime) -> int:
        """Computes the index into the _available_index_timestamps where start lies in"""
        return min(
            self._available_index_timestamps.index(
                [
                    timestamp
                    for timestamp in self._available_index_timestamps
                    if self.timestamp_to_dt(timestamp) <= end
                ][-1]
            )
            + 1,
            len(self._available_index_timestamps) - 1,
        )

    def _start_iteration_index(self, start: datetime) -> int:
        """Computes the index into _loaded_data to start from
        when you want to start iterating over it given the start datetime
        """
        return [
            i for i in range(len(self._loaded_data)) if self._loaded_data[i][0] >= start
        ][0]

    def _load_data_between(self, start: datetime, end: datetime):
        """Loads all data between the given datetime into the cache"""
        start_index = self._start_index(start)
        end_index = self._end_index(end)
        for index_timestamp in self._available_index_timestamps[
            start_index : end_index + 1
        ]:
            if index_timestamp in self._loaded_data_index_timestamps:
                continue
            self._load_data(index_timestamp)

    def data_available(
        self, start: datetime, end: datetime
    ) -> tuple[bool, tuple[datetime | None, datetime | None]]:
        """Checks if data is available in the given interval and returns True if so.
        It also returns the interval for which data is available. This is useful
        if data is only available for a queried subinterval.
        """
        if end < start:
            return False, (None, None)
        self._load_data_between(start, end)
        found_start = None
        found_end = None
        for idx in range(self._start_iteration_index(start), len(self._loaded_data)):
            dt, value = self._loaded_data[idx]
            if dt > end:
                return True, (found_start, found_end)
            if value:
                found_start = dt if not found_start else found_start
            else:
                return (
                    (True, (found_start, found_end))
                    if found_end
                    else (False, (None, None))
                )
            found_end = dt

        return True, (found_start, found_end)

    def get_data(self, start: datetime, end: datetime) -> list[tuple[datetime, float]]:
        """Returns data for the queried interval."""
        available, (start, end) = self.data_available(start, end)
        if not available:
            return []
        start_iteration_index = self._start_iteration_index(start)
        return [
            self._loaded_data[i]
            for i in range(
                start_iteration_index, len(self._loaded_data)  # - start_iteration_index
            )
            if self._loaded_data[i][0] <= end
        ]


start = datetime(2023, 4, 1, 0, 0, 0, tzinfo=pytz.timezone("Europe/Berlin"))
end = datetime(2023, 4, 3, 23, 59, 59, tzinfo=pytz.timezone("Europe/Berlin"))
data_provider = DataProvider()
is_availabe, (start, end) = data_provider.data_available(start, end)
print(start)
print(end)
electricity_production = data_provider.get_data(start, end)

time = [dt for dt, _ in electricity_production]
electricity = [value for _, value in electricity_production]

plt.plot(time, electricity, "r")
plt.xlabel("Time")
plt.ylabel("Electricity production in MWh")
plt.xticks(rotation=45)
plt.show()
