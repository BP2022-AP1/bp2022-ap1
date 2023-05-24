import marshmallow as marsh
import peewee
import pytest

from src.schedule.schedule_configuration import (
    ScheduleConfiguration,
    ScheduleConfigurationXSimulationPlatform,
)
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


@pytest.mark.parametrize(
    "schedule_data", [("regular_train_schedule_data"), ("random_train_schedule_data")]
)
class TestScheduleConfigurationModel:
    """Test (de)serialization and database access of ScheduleConfiguration"""

    @recreate_db_setup
    def setup_method(self):
        pass

    def test_db_interaction(self, schedule_data: dict, request: pytest.FixtureRequest):
        schedule_data = request.getfixturevalue(schedule_data)
        schedule_configuration = ScheduleConfiguration(**schedule_data)
        schedule_configuration.save(force_insert=True)
        fetched = (
            ScheduleConfiguration.select()
            .where(ScheduleConfiguration.id == schedule_configuration.id)
            .first()
        )
        for key in schedule_data:
            assert getattr(schedule_configuration, key) == getattr(fetched, key)

    def test_serialization(self, schedule_data: dict, request: pytest.FixtureRequest):
        schedule_data = request.getfixturevalue(schedule_data)
        schedule_configuration = ScheduleConfiguration(**schedule_data)
        serialized = schedule_configuration.to_dict()
        for key, value in schedule_data.items():
            assert serialized[key] == value
        assert serialized["platforms"] == []


@pytest.mark.parametrize(
    "obj",
    [({})],
)
class TestScheduleConfigurationXSimulationPlatformFail:
    """Test that the TestScheduleConfigurationXSimulationPlatformFail fails when fields are missing"""

    @recreate_db_setup
    def setup_method(self):
        pass

    def test_create(self, obj: dict):
        """Test that an object of a class cannot be created."""
        with pytest.raises(peewee.IntegrityError):
            ScheduleConfigurationXSimulationPlatform.create(
                **obj,
            )


class TestScheduleConfigurationXSimulationPlatformModel:
    """Test (de)serialization and database access of ScheduleConfigurationXSimulationPlatform"""

    @recreate_db_setup
    def setup_method(self):
        pass

    @pytest.fixture
    def schedule_configuration(
        self, regular_train_schedule_data: dict
    ) -> ScheduleConfiguration:
        configuration = ScheduleConfiguration(**regular_train_schedule_data)
        configuration.save()
        return configuration

    @pytest.fixture
    def object_dict(
        self, schedule_configuration: ScheduleConfiguration, platform_ids: list[str]
    ):
        return {
            "schedule_configuration_id": schedule_configuration.id,
            "simulation_platform_id": platform_ids[0],
            "index": 0,
        }

    @pytest.fixture
    def obj(self, object_dict: dict) -> ScheduleConfigurationXSimulationPlatform:
        return ScheduleConfigurationXSimulationPlatform(**object_dict)

    def test_db_interaction(
        self, object_dict: dict, obj: ScheduleConfigurationXSimulationPlatform
    ):
        obj.save()
        fetched = (
            ScheduleConfigurationXSimulationPlatform.select()
            .where(ScheduleConfigurationXSimulationPlatform.id == obj.id)
            .first()
        )
        for key in object_dict:
            assert str(getattr(obj, key)) == str(getattr(fetched, key))
