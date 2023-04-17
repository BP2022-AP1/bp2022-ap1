# pylint: disable=unused-argument

import marshmallow as marsh
import peewee
import pytest

from src.schedule.schedule_configuration import ScheduleConfiguration
from tests.decorators import recreate_db_setup


@pytest.mark.parametrize(
    "obj",
    [({})],
)
class TestScheduleConfigurationFail:
    """Test that the ScheduleConfiguration fails when fields are missing"""

    @recreate_db_setup
    def setup_method(self):
        pass

    def test_create(self, obj: dict):
        """Test that an object of a class cannot be created."""
        with pytest.raises(peewee.IntegrityError):
            ScheduleConfiguration.create(
                **obj,
            )

    def test_deserialization(self, obj: dict):
        """Test that an object of a class cannot be deserialized."""
        with pytest.raises(marsh.exceptions.ValidationError):
            ScheduleConfiguration.Schema().load(obj)


@pytest.mark.parametrize(
    "in_dict,obj_dict,out_dict",
    [
        (
            {
                "schedule_type": "TrainSchedule",
                "strategy_type": "RegularScheduleStrategy",
                "strategy_start_tick": 10,
                "strategy_end_tick": 1000,
                "train_schedule_train_type": "cargo",
                "regular_strategy_frequency": 100,
            },
            {
                "schedule_type": "TrainSchedule",
                "strategy_type": "RegularScheduleStrategy",
                "strategy_start_tick": 10,
                "strategy_end_tick": 1000,
                "train_schedule_train_type": "cargo",
                "regular_strategy_frequency": 100,
            },
            {
                "schedule_type": "TrainSchedule",
                "strategy_type": "RegularScheduleStrategy",
                "strategy_start_tick": 10,
                "strategy_end_tick": 1000,
                "train_schedule_train_type": "cargo",
                "regular_strategy_frequency": 100,
            },
        ),
        (
            {
                "schedule_type": "TrainSchedule",
                "strategy_type": "RandomScheduleStrategy",
                "strategy_start_tick": 10,
                "strategy_end_tick": 1000,
                "train_schedule_train_type": "cargo",
                "random_strategy_trains_per_1000_ticks": 10.0,
                "random_strategy_seed": 42,
            },
            {
                "schedule_type": "TrainSchedule",
                "strategy_type": "RandomScheduleStrategy",
                "strategy_start_tick": 10,
                "strategy_end_tick": 1000,
                "train_schedule_train_type": "cargo",
                "random_strategy_trains_per_1000_ticks": 10.0,
                "random_strategy_seed": 42,
            },
            {
                "schedule_type": "TrainSchedule",
                "strategy_type": "RandomScheduleStrategy",
                "strategy_start_tick": 10,
                "strategy_end_tick": 1000,
                "train_schedule_train_type": "cargo",
                "random_strategy_trains_per_1000_ticks": 10.0,
                "random_strategy_seed": 42,
            },
        ),
    ],
)
class TestScheduleConfigurationModel:
    """Test the ScheduleConfiguration"""

    @recreate_db_setup
    def setup_method(self):
        pass

    def test_deserialization(self, in_dict: dict, obj_dict: dict, out_dict: dict):
        schedule_configuration = ScheduleConfiguration.from_dict(in_dict)
        for key, value in obj_dict.items():
            assert getattr(schedule_configuration, key) == value

    def test_db_interaction(self, in_dict: dict, obj_dict: dict, out_dict: dict):
        schedule_configuration = ScheduleConfiguration.from_dict(in_dict)
        schedule_configuration.save(force_insert=True)
        fetched = (
            ScheduleConfiguration.select()
            .where(ScheduleConfiguration.id == schedule_configuration.id)
            .first()
        )
        for key in obj_dict:
            assert getattr(schedule_configuration, key) == getattr(fetched, key)

    def test_serialization(self, in_dict: dict, obj_dict: dict, out_dict: dict):
        schedule_configuration = ScheduleConfiguration.from_dict(in_dict)
        serialized = schedule_configuration.to_dict()
        for key, value in out_dict.items():
            assert serialized[key] == value
