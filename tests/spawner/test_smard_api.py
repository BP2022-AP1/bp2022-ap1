from datetime import datetime

import marshmallow as marsh
import peewee
import pytest

from src.schedule.smard_api import SmardApi, SmardApiEntry, SmardApiIndex
from tests.decorators import recreate_db_setup


@pytest.mark.parametrize(
    "obj",
    [({})],
)
class TestSmardApiIndexFail:
    @recreate_db_setup
    def setup_method(self):
        pass

    def test_create(self, obj: dict):
        """Test that an object of a class cannot be created."""
        with pytest.raises(peewee.IntegrityError):
            SmardApiIndex.create(
                **obj,
            )

    def test_deserialization(self, obj: dict):
        """Test that an object of a class cannot be deserialized."""
        with pytest.raises(marsh.exceptions.ValidationError):
            SmardApiIndex.Schema().load(obj)


@pytest.mark.parametrize("obj", [({"timestamp": datetime.now().isoformat()})])
class TestSmardApiIndexModel:
    @recreate_db_setup
    def setup_method(self):
        pass

    def test_deserialization(self, obj: dict):
        index = SmardApiIndex.from_dict(obj)
        assert index.timestamp.isoformat() == obj["timestamp"]

    def test_db_interaction(self, obj: dict):
        index = SmardApiIndex.from_dict(obj)
        index.save()
        fetched = SmardApiIndex.select().where(SmardApiIndex.id == index.id).first()
        for key in obj:
            assert getattr(index, key) == getattr(fetched, key)

    def test_serialization(self, obj: dict):
        index = SmardApiIndex.from_dict(obj)
        serialized = index.to_dict()
        for key, value in obj.items():
            assert serialized[key] == value


@pytest.mark.parametrize(
    "obj",
    [({})],
)
class TestSmardApiEntryFail:
    @recreate_db_setup
    def setup_method(self):
        pass

    def test_create(self, obj: dict):
        """Test that an object of a class cannot be created."""
        with pytest.raises(peewee.IntegrityError):
            SmardApiEntry.create(
                **obj,
            )

    def test_deserialization(self, obj: dict):
        """Test that an object of a class cannot be deserialized."""
        with pytest.raises(marsh.exceptions.ValidationError):
            SmardApiEntry.Schema().load(obj)


@pytest.mark.parametrize(
    "obj", [({"timestamp": datetime.now().isoformat(), "value": 42.0})]
)
class TestSmardApiEntryModel:
    _index: SmardApiIndex

    @recreate_db_setup
    def setup_method(self):
        self._index = SmardApiIndex.create(timestamp=datetime.now())

    def test_deserialization(self, obj: dict):
        obj["index_id"] = self._index.id
        entry = SmardApiEntry.from_dict(obj)
        assert entry.timestamp.isoformat() == obj["timestamp"]
        assert entry.value == obj["value"]
        assert entry.index_id == self._index

    def test_db_interaction(self, obj: dict):
        obj["index_id"] = self._index.id
        entry = SmardApiEntry.from_dict(obj)
        entry.save()
        fetched = SmardApiEntry.select().where(SmardApiEntry.id == entry.id).first()
        for key in obj:
            assert getattr(entry, key) == getattr(fetched, key)

    def test_serialization(self, obj: dict):
        obj["index_id"] = self._index.id
        entry = SmardApiEntry.from_dict(obj)
        serialized = entry.to_dict()
        for key, value in obj.items():
            assert str(serialized[key]) == str(value)


class TestSmardApi:
    """Test the SMARD API"""

    @recreate_db_setup
    def setup_method(self):
        pass

    @pytest.mark.usefixtures("demand_strategy_available_interval")
    def test_data_available(
        self, demand_strategy_available_interval: tuple[datetime, datetime]
    ):
        start, end = demand_strategy_available_interval
        availability = SmardApi().data_availability(start, end)
        assert availability.available
        assert not availability.interval_altered
        assert availability.start >= start
        assert availability.start <= end
        assert availability.end >= start
        assert availability.end <= end
        assert availability.start <= availability.end

    @pytest.mark.usefixtures("demand_strategy_not_available_past_interval")
    def test_no_data_available(
        self, demand_strategy_not_available_past_interval: tuple[datetime, datetime]
    ):
        start, end = demand_strategy_not_available_past_interval
        availability = SmardApi().data_availability(start, end)
        assert not availability.available

    @pytest.mark.usefixtures("demand_strategy_not_available_future_interval")
    def test_no_data_available(
        self, demand_strategy_not_available_future_interval: tuple[datetime, datetime]
    ):
        start, end = demand_strategy_not_available_future_interval
        availability = SmardApi().data_availability(start, end)
        assert not availability.available

    @pytest.mark.usefixtures("demand_strategy_available_interval")
    def test_negative_length_interval(
        self, demand_strategy_available_interval: tuple[datetime, datetime]
    ):
        start, end = demand_strategy_available_interval
        availability = SmardApi().data_availability(end, start)
        assert not availability.available

    @pytest.mark.usefixtures("demand_strategy_start_not_available_interval")
    def test_start_not_available(
        self, demand_strategy_start_not_available_interval: tuple[datetime, datetime]
    ):
        start, end = demand_strategy_start_not_available_interval
        availability = SmardApi().data_availability(start, end)
        assert availability.available
        assert availability.interval_altered
        assert availability.start >= start
        assert availability.start <= end
        assert availability.end >= start
        assert availability.end <= end
        assert availability.start <= availability.end

    @pytest.mark.usefixtures("demand_strategy_end_not_available_interval")
    def test_end_not_available(
        self, demand_strategy_end_not_available_interval: tuple[datetime, datetime]
    ):
        start, end = demand_strategy_end_not_available_interval
        availability = SmardApi().data_availability(start, end)
        assert availability.available
        assert availability.interval_altered
        assert availability.start >= start
        assert availability.start <= end
        assert availability.end >= start
        assert availability.end <= end
        assert availability.start <= availability.end

    @pytest.mark.usefixtures("demand_strategy_all_none_interval")
    def test_all_none(
        self, demand_strategy_all_none_interval: tuple[datetime, datetime]
    ):
        start, end = demand_strategy_all_none_interval
        availability = SmardApi().data_availability(start, end)
        assert not availability.available

    @pytest.mark.usefixtures("demand_strategy_available_interval")
    def test_get_data(
        self, demand_strategy_available_interval: tuple[datetime, datetime]
    ):
        start, end = demand_strategy_available_interval
        data = SmardApi().get_data(start, end)
        assert len(data) > 0
        assert data[0].timestamp >= start
        assert data[-1].timestamp <= end

    @pytest.mark.usefixtures("demand_strategy_not_available_past_interval")
    def test_dont_get_data(
        self, demand_strategy_not_available_past_interval: tuple[datetime, datetime]
    ):
        start, end = demand_strategy_not_available_past_interval
        data = SmardApi().get_data(start, end)
        assert len(data) == 0
