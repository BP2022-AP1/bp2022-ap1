import pytest

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
    def train(self) -> Train:
        return Train("fault injector train")

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
        wrapper: SimulationObjectUpdatingComponent,
        interlocking: IInterlockingDisruptor,
    ):
        return TrainSpeedFault(
            configuration=train_speed_fault_configuration,
            logger=logger,
            wrapper=wrapper,
            interlocking=interlocking,
        )

    def test_inject_train_speed_fault(
        self,
        tick,
        train_speed_fault: TrainSpeedFault,
        train: Train,
        # the following argument is a needed fixture
        # pylint: disable-next=unused-argument
        combine_train_and_wrapper,
    ):
        train.speed = 100
        assert train.speed == 100
        with pytest.raises(NotImplementedError):
            train_speed_fault.inject_fault(tick=tick)
        assert train.speed == train_speed_fault.configuration.new_speed

    def test_resolve_train_speed_fault(
        self,
        tick,
        train_speed_fault: TrainSpeedFault,
        train: Train,
        # the following argument is a needed fixture
        # pylint: disable-next=unused-argument
        combine_train_and_wrapper,
    ):
        train.speed = 50
        with pytest.raises(NotImplementedError):
            train_speed_fault.inject_fault(tick=tick)
        assert train.speed == train_speed_fault.configuration.new_speed
        with pytest.raises(NotImplementedError):
            train_speed_fault.resolve_fault(tick=tick)
        assert train.speed == train_speed_fault.old_speed == 50
