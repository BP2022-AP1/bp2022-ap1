import pytest
from traci import vehicle

from src.fault_injector.fault_configurations.train_speed_fault_configuration import (
    TrainSpeedFaultConfiguration,
)
from src.fault_injector.fault_types.train_speed_fault import TrainSpeedFault
from src.interlocking_component.route_controller import IInterlockingDisruptor
from src.logger.logger import Logger
from src.wrapper.simulation_object_updating_component import (
    SimulationObjectUpdatingComponent,
)
from src.wrapper.simulation_objects import Train
from tests.decorators import recreate_db_setup


class TestTrainSpeedFault:
    """Tests for TrainSpeedFault"""

    @recreate_db_setup
    def setup_method(self):
        pass

    @pytest.fixture
    def train_speed_fault_configuration(self, train: Train):
        return TrainSpeedFaultConfiguration.create(
            **{
                "start_tick": 40,
                "end_tick": 400,
                "description": "test TrainSpeedFault",
                "affected_element_id": train.identifier,
                "new_speed": 30,
            }
        )

    @pytest.fixture
    def train_speed_fault(
        self,
        train_speed_fault_configuration: TrainSpeedFaultConfiguration,
        logger: Logger,
        simulation_object_updater: SimulationObjectUpdatingComponent,
        interlocking: IInterlockingDisruptor,
    ):
        return TrainSpeedFault(
            configuration=train_speed_fault_configuration,
            logger=logger,
            simulation_object_updater=simulation_object_updater,
            interlocking=interlocking,
        )

    @pytest.fixture
    def max_speed(self, monkeypatch):
        # pylint: disable-next=unused-argument
        def set_max_speed(train_id: str, speed: float):
            pass

        monkeypatch.setattr(vehicle, "setMaxSpeed", set_max_speed)

    def test_inject_train_speed_fault(
        self,
        tick,
        train_speed_fault: TrainSpeedFault,
        train: Train,
        # the following arguments are needed fixtures
        # pylint: disable=unused-argument
        max_speed,
        train_add,
        combine_train_and_wrapper,
        # pylint: enable=unused-argument
    ):
        train.train_type.max_speed = 100
        with pytest.raises(NotImplementedError):
            train_speed_fault.inject_fault(tick=tick)
        assert train.train_type.max_speed == train_speed_fault.configuration.new_speed

    def test_resolve_train_speed_fault(
        self,
        tick,
        train_speed_fault: TrainSpeedFault,
        train: Train,
        # the following arguments are needed fixtures
        # pylint: disable=unused-argument
        max_speed,
        train_add,
        combine_train_and_wrapper,
        # pylint: enable=unused-argument
    ):
        train.train_type.max_speed = 50
        with pytest.raises(NotImplementedError):
            train_speed_fault.inject_fault(tick=tick)
        assert train.train_type.max_speed == train_speed_fault.configuration.new_speed
        with pytest.raises(NotImplementedError):
            train_speed_fault.resolve_fault(tick=tick)
        assert train.train_type.max_speed == train_speed_fault.old_speed == 50
