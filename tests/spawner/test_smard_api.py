from datetime import datetime

import peewee
import pytest

from src.schedule.smard_api import SmardApiEntry, SmardApiIndex
from tests.decorators import recreate_db_setup


@pytest.mark.parametrize(
    "obj",
    [({})],
)
class TestSmardApiIndexFail:
    """Test the SmardApiIndex class."""

    @recreate_db_setup
    def setup_method(self):
        pass

    def test_create(self, obj: dict):
        """Test that an object of a class cannot be created."""
        with pytest.raises(peewee.IntegrityError):
            SmardApiIndex.create(
                **obj,
            )


@pytest.mark.parametrize("obj", [({"timestamp": datetime(2015, 1, 19, 0, 0)})])
class TestSmardApiIndexModel:
    """Test the SmardApiIndex class."""

    @recreate_db_setup
    def setup_method(self):
        pass

    def test_db_interaction(self, obj: dict):
        index = SmardApiIndex(**obj)
        index.save()
        fetched = SmardApiIndex.select().where(SmardApiIndex.id == index.id).first()
        for key in obj:
            assert getattr(index, key) == getattr(fetched, key)


@pytest.mark.parametrize(
    "obj",
    [({})],
)
class TestSmardApiEntryFail:
    """Test the SmardApiEntry class."""

    @recreate_db_setup
    def setup_method(self):
        pass

    def test_create(self, obj: dict):
        """Test that an object of a class cannot be created."""
        with pytest.raises(peewee.IntegrityError):
            SmardApiEntry.create(
                **obj,
            )


@pytest.mark.parametrize(
    "obj", [({"timestamp": datetime(2015, 1, 19, 0, 0), "value": 42.0})]
)
class TestSmardApiEntryModel:
    """Test the SmardApiEntry class."""

    _index: SmardApiIndex

    @recreate_db_setup
    def setup_method(self):
        self._index = SmardApiIndex.create(timestamp=datetime.fromtimestamp(1421622000))

    def test_db_interaction(self, obj: dict):
        obj["index_id"] = self._index.id
        entry = SmardApiEntry(**obj)
        entry.save()
        fetched = SmardApiEntry.select().where(SmardApiEntry.id == entry.id).first()
        for key in obj:
            assert getattr(entry, key) == getattr(fetched, key)


class TestSmardApi:
    """Test the SMARD API"""

    @recreate_db_setup
    def setup_method(self):
        pass

    def test_data_available(
        self,
        monkeypatched_smard_api: object,
        demand_strategy_available_interval: tuple[datetime, datetime],
    ):
        start, end = demand_strategy_available_interval
        availability = monkeypatched_smard_api.data_availability(start, end)
        assert availability.available
        assert not availability.interval_altered
        assert availability.start >= start
        assert availability.start <= end
        assert availability.end >= start
        assert availability.end <= end
        assert availability.start <= availability.end

    def test_no_data_available(
        self,
        monkeypatched_smard_api: object,
        demand_strategy_not_available_past_interval: tuple[datetime, datetime],
    ):
        start, end = demand_strategy_not_available_past_interval
        availability = monkeypatched_smard_api.data_availability(start, end)
        assert not availability.available

    def test_negative_length_interval(
        self,
        monkeypatched_smard_api: object,
        demand_strategy_available_interval: tuple[datetime, datetime],
    ):
        start, end = demand_strategy_available_interval
        availability = monkeypatched_smard_api.data_availability(end, start)
        assert not availability.available

    def test_start_not_available(
        self,
        monkeypatched_smard_api: object,
        demand_strategy_start_not_available_interval: tuple[datetime, datetime],
    ):
        start, end = demand_strategy_start_not_available_interval
        availability = monkeypatched_smard_api.data_availability(start, end)
        assert availability.available
        assert availability.interval_altered
        assert availability.start >= start
        assert availability.start <= end
        assert availability.end >= start
        assert availability.end <= end
        assert availability.start <= availability.end

    def test_end_not_available(
        self,
        monkeypatched_smard_api: object,
        demand_strategy_end_not_available_interval: tuple[datetime, datetime],
    ):
        start, end = demand_strategy_end_not_available_interval
        availability = monkeypatched_smard_api.data_availability(start, end)
        assert availability.available
        assert availability.interval_altered
        assert availability.start >= start
        assert availability.start <= end
        assert availability.end >= start
        assert availability.end <= end
        assert availability.start <= availability.end

    def test_all_none(
        self,
        monkeypatched_smard_api: object,
        demand_strategy_all_none_interval: tuple[datetime, datetime],
    ):
        start, end = demand_strategy_all_none_interval
        availability = monkeypatched_smard_api.data_availability(start, end)
        assert not availability.available

    def test_get_data(
        self,
        monkeypatched_smard_api: object,
        demand_strategy_available_interval: tuple[datetime, datetime],
    ):
        start, end = demand_strategy_available_interval
        data = monkeypatched_smard_api.get_data(start, end)
        assert len(data) > 0
        assert data[0].timestamp >= start
        assert data[-1].timestamp <= end

    def test_dont_get_data(
        self,
        monkeypatched_smard_api: object,
        demand_strategy_not_available_past_interval: tuple[datetime, datetime],
    ):
        start, end = demand_strategy_not_available_past_interval
        data = monkeypatched_smard_api.get_data(start, end)
        assert len(data) == 0
