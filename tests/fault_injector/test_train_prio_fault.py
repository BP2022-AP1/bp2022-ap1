import pytest

from src.fault_injector.fault_configurations.train_prio_fault_configuration import (
    TrainPrioFaultConfiguration,
)
from src.fault_injector.fault_types.train_prio_fault import TrainPrioFault
from src.interlocking_component.route_controller import IInterlockingDisruptor
from src.logger.logger import Logger
from src.wrapper.simulation_object_updating_component import (
    SimulationObjectUpdatingComponent,
)
from src.wrapper.simulation_objects import Train
from tests.decorators import recreate_db_setup


class TestTrainPrioFault:
    """Tests for TrainPrioFault"""

    @recreate_db_setup
    def setup_method(self):
        pass

    @pytest.fixture
    def train_prio_fault_configuration(self, train: Train):
        return TrainPrioFaultConfiguration.create(
            **{
                "start_tick": 50,
                "end_tick": 500,
                "description": "test TrainPrioFault",
                "affected_element_id": train.identifier,
                "new_prio": 3,
            }
        )

    @pytest.fixture
    def train_prio_fault(
        self,
        train_prio_fault_configuration: TrainPrioFaultConfiguration,
        logger: Logger,
        wrapper: SimulationObjectUpdatingComponent,
        interlocking: IInterlockingDisruptor,
    ):
        return TrainPrioFault(
            configuration=train_prio_fault_configuration,
            logger=logger,
            wrapper=wrapper,
            interlocking=interlocking,
        )

    def test_inject_train_prio_fault(
        self,
        tick,
        train_prio_fault: TrainPrioFault,
        train: Train,
        # the following argument is a needed fixture
        # pylint: disable-next=unused-argument
        combine_train_and_wrapper,
    ):
        train.train_type.priority = 1
        with pytest.raises(NotImplementedError):
            train_prio_fault.inject_fault(tick)
        assert train.train_type.priority == train_prio_fault.configuration.new_prio

    def test_resolve_train_prio_fault(
        self,
        tick,
        train_prio_fault: TrainPrioFault,
        train: Train,
        # the following argument is a needed fixture
        # pylint: disable-next=unused-argument
        combine_train_and_wrapper,
    ):
        train.train_type.priority = 5
        with pytest.raises(NotImplementedError):
            train_prio_fault.inject_fault(tick)
        assert train.train_type.priority == train_prio_fault.configuration.new_prio
        with pytest.raises(NotImplementedError):
            train_prio_fault.resolve_fault(tick)
        assert train.train_type.priority == train_prio_fault.old_prio == 5
