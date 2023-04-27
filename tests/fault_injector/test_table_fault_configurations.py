from uuid import UUID

import marshmallow as marsh
import peewee
import pytest

from src.base_model import BaseModel
from src.fault_injector.fault_configurations.fault_configuration import (
    FaultConfiguration,
)
from src.fault_injector.fault_configurations.platform_blocked_fault_configuration import (
    PlatformBlockedFaultConfiguration,
    PlatformBlockedFaultConfigurationXSimulationConfiguration,
)
from src.fault_injector.fault_configurations.schedule_blocked_fault_configuration import (
    ScheduleBlockedFaultConfiguration,
    ScheduleBlockedFaultConfigurationXSimulationConfiguration,
)
from src.fault_injector.fault_configurations.track_blocked_fault_configuration import (
    TrackBlockedFaultConfiguration,
    TrackBlockedFaultConfigurationXSimulationConfiguration,
)
from src.fault_injector.fault_configurations.track_speed_limit_fault_configuration import (
    TrackSpeedLimitFaultConfiguration,
    TrackSpeedLimitFaultConfigurationXSimulationConfiguration,
)
from src.fault_injector.fault_configurations.train_prio_fault_configuration import (
    TrainPrioFaultConfiguration,
    TrainPrioFaultConfigurationXSimulationConfiguration,
)
from src.fault_injector.fault_configurations.train_speed_fault_configuration import (
    TrainSpeedFaultConfiguration,
    TrainSpeedFaultConfigurationXSimulationConfiguration,
)
from src.implementor.models import SimulationConfiguration
from tests.decorators import recreate_db_setup

# pylint: disable=duplicate-code
# will change, when adding foreign keys


@pytest.mark.parametrize(
    "table_class, object_as_dict",
    [
        (PlatformBlockedFaultConfiguration, {}),
        (TrainSpeedFaultConfiguration, {}),
        (ScheduleBlockedFaultConfiguration, {}),
        (TrackBlockedFaultConfiguration, {}),
        (TrainPrioFaultConfiguration, {}),
        (TrackSpeedLimitFaultConfiguration, {}),
    ],
)
class TestFailingDict:
    """Test that a object of a class cannot be created or deserialized with invalid data."""

    @recreate_db_setup
    def setup_method(self):
        pass

    def test_create(self, table_class: BaseModel, object_as_dict: dict):
        """Test that an object of a class cannot be created."""
        with pytest.raises(peewee.IntegrityError):
            table_class.create(
                **object_as_dict,
            )

    def test_deserialization(self, table_class: BaseModel, object_as_dict: dict):
        """Test that an object of a class cannot be deserialized."""
        with pytest.raises(marsh.exceptions.ValidationError):
            table_class.Schema().load(object_as_dict)


@pytest.mark.parametrize(
    "table_class, object_as_dict",
    [
        (
            TrainSpeedFaultConfiguration,
            {
                "start_tick": 1,
                "end_tick": 100,
                "description": "TrainSpeedFault",
                "affected_element_id": "12345678",
                "new_speed": 40,
                "strategy": "regular",
            },
        ),
        (
            PlatformBlockedFaultConfiguration,
            {
                "start_tick": 1,
                "end_tick": 100,
                "description": "PlatformBlockedFault",
                "affected_element_id": "12345678",
                "strategy": "regular",
            },
        ),
        (
            ScheduleBlockedFaultConfiguration,
            {
                "start_tick": 1,
                "end_tick": 100,
                "description": "ScheduleBlockedFault",
                "affected_element_id": "12345678",
                "strategy": "regular",
            },
        ),
        (
            TrackBlockedFaultConfiguration,
            {
                "start_tick": 1,
                "end_tick": 100,
                "description": "TrackBlockedFault",
                "affected_element_id": "12345678",
                "strategy": "regular",
            },
        ),
        (
            TrainPrioFaultConfiguration,
            {
                "start_tick": 1,
                "end_tick": 100,
                "description": "TrainPrioFault",
                "affected_element_id": "12345678",
                "new_prio": 1,
                "strategy": "regular",
            },
        ),
        (
            TrackSpeedLimitFaultConfiguration,
            {
                "start_tick": 1,
                "end_tick": 100,
                "description": "TrackSpeedLimitFault",
                "affected_element_id": "12345678",
                "new_speed_limit": 60,
                "strategy": "regular",
            },
        ),
    ],
)
class TestCorrectFilledDict:
    """Test that a object of a class can be created and deserialized with valid data."""

    @recreate_db_setup
    def setup_method(self):
        pass

    def test_create(self, table_class: BaseModel, object_as_dict: dict):
        """Test that a object of a class can be created."""
        obj = table_class.create(
            **object_as_dict,
        )
        assert table_class.select().where(table_class.id == obj.id).first() == obj

    def test_serialization(self, table_class: BaseModel, object_as_dict: dict):
        """Test that an object of a class can be serialized."""
        serialized_obj = table_class.create(
            **object_as_dict,
        ).to_dict()

        for key in object_as_dict.keys():
            assert serialized_obj[key] == object_as_dict[key]

        none_fields = (
            set(table_class.Schema().fields.keys())
            - set(object_as_dict.keys())
            - set(["id", "created_at", "updated_at"])
        )
        for key in none_fields:
            assert serialized_obj[key] is None

    def test_deserialization_full_dict(
        self, table_class: BaseModel, object_as_dict: dict
    ):
        """Test that an object of a class can be deserialized."""
        obj = table_class.Schema().load(
            object_as_dict,
        )
        assert isinstance(obj, table_class)
        assert isinstance(obj.id, UUID)
        for key in object_as_dict.keys():
            assert getattr(obj, key) == object_as_dict[key]


@pytest.mark.parametrize(
    "fault_configuration, relationship_class, relationship_name",
    [
        (
            TrainSpeedFaultConfiguration(
                **{
                    "start_tick": 1,
                    "end_tick": 100,
                    "description": "TrainSpeedFault",
                    "affected_element_id": "12345678",
                    "new_speed": 40,
                }
            ),
            TrainSpeedFaultConfigurationXSimulationConfiguration,
            "train_speed_fault_configuration",
        ),
        (
            PlatformBlockedFaultConfiguration(
                **{
                    "start_tick": 1,
                    "end_tick": 100,
                    "description": "PlatformBlockedFault",
                    "affected_element_id": "12345678",
                }
            ),
            PlatformBlockedFaultConfigurationXSimulationConfiguration,
            "platform_blocked_fault_configuration",
        ),
        (
            ScheduleBlockedFaultConfiguration(
                **{
                    "start_tick": 1,
                    "end_tick": 100,
                    "description": "ScheduleBlockedFault",
                    "affected_element_id": "12345678",
                }
            ),
            ScheduleBlockedFaultConfigurationXSimulationConfiguration,
            "schedule_blocked_fault_configuration",
        ),
        (
            TrackBlockedFaultConfiguration(
                **{
                    "start_tick": 1,
                    "end_tick": 100,
                    "description": "TrackBlockedFault",
                    "affected_element_id": "12345678",
                }
            ),
            TrackBlockedFaultConfigurationXSimulationConfiguration,
            "track_blocked_fault_configuration",
        ),
        (
            TrainPrioFaultConfiguration(
                **{
                    "start_tick": 1,
                    "end_tick": 100,
                    "description": "TrainPrioFault",
                    "affected_element_id": "12345678",
                    "new_prio": 1,
                }
            ),
            TrainPrioFaultConfigurationXSimulationConfiguration,
            "train_prio_fault_configuration",
        ),
        (
            TrackSpeedLimitFaultConfiguration(
                **{
                    "start_tick": 1,
                    "end_tick": 100,
                    "description": "TrackSpeedLimitFault",
                    "affected_element_id": "12345678",
                    "new_speed_limit": 60,
                }
            ),
            TrackSpeedLimitFaultConfigurationXSimulationConfiguration,
            "track_speed_limit_fault_configuration",
        ),
    ],
)
class TestFaultConfigurationRelationship:
    """Test that a object of a class can be created and deserialized with valid data."""

    @recreate_db_setup
    def setup_method(self):
        pass

    def test_relationship_creation(
        self,
        simulation_configuration: SimulationConfiguration,
        fault_configuration: FaultConfiguration,
        relationship_class,
        relationship_name,
    ):
        fault_configuration.save()
        fault_x_simulation = relationship_class(
            **{
                relationship_name: fault_configuration,
                "simulation_configuration": simulation_configuration,
            }
        )
        fault_x_simulation.save()
        assert getattr(fault_x_simulation, relationship_name) == fault_configuration
        assert fault_x_simulation.simulation_configuration == simulation_configuration

    def test_relationship_back_references(
        self,
        simulation_configuration: SimulationConfiguration,
        fault_configuration: FaultConfiguration,
        relationship_class,
        relationship_name,
    ):
        fault_configuration.save()
        fault_x_simulation = relationship_class(
            **{
                relationship_name: fault_configuration,
                "simulation_configuration": simulation_configuration,
            }
        )
        fault_x_simulation.save()
        assert (
            len(getattr(simulation_configuration, f"{relationship_name}_references"))
            == 1
        )
        assert (
            getattr(simulation_configuration, f"{relationship_name}_references")[0]
            == fault_x_simulation
        )
        assert len(fault_configuration.simulation_configuration_references) == 1
        assert (
            fault_configuration.simulation_configuration_references[0]
            == fault_x_simulation
        )

    def test_relationship_serialization(
        self,
        simulation_configuration: SimulationConfiguration,
        fault_configuration: FaultConfiguration,
        relationship_class,
        relationship_name,
    ):
        fault_configuration.save()
        fault_x_simulation = relationship_class(
            **{
                relationship_name: fault_configuration,
                "simulation_configuration": simulation_configuration,
            }
        )
        fault_x_simulation.save()
        obj_dict = fault_x_simulation.to_dict()
        del obj_dict["created_at"]
        del obj_dict["updated_at"]

        assert obj_dict == {
            "id": str(fault_x_simulation.id),
            "simulation_configuration": str(simulation_configuration.id),
            relationship_name: str(fault_configuration.id),
        }

    def test_relationship_deserialization(
        self,
        simulation_configuration: SimulationConfiguration,
        fault_configuration: FaultConfiguration,
        relationship_class,
        relationship_name,
    ):
        fault_configuration.save()
        fault_x_simulation = relationship_class.from_dict(
            {
                relationship_name: str(fault_configuration.id),
                "simulation_configuration": str(simulation_configuration.id),
            }
        )
        fault_x_simulation.save()
        assert getattr(fault_x_simulation, relationship_name) == fault_configuration
        assert fault_x_simulation.simulation_configuration == simulation_configuration
