import pytest

from src.event_bus.event_bus import EventBus
from src.fault_injector.fault_configurations.train_prio_fault_configuration import (
    TrainPrioFaultConfiguration,
)
from src.fault_injector.fault_types.train_prio_fault import TrainPrioFault
from src.interlocking_component.route_controller import IInterlockingDisruptor
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
    def train_prio_fault_configuration(self, basic_train):
        return TrainPrioFaultConfiguration.create(
            **{
                "start_time": 50,
                "end_time": 500,
                "description": "test TrainPrioFault",
                "affected_element_id": basic_train.identifier,
                "new_prio": 3,
                "strategy": "regular",
            }
        )

    @pytest.fixture
    def train_prio_fault(
        self,
        train_prio_fault_configuration: TrainPrioFaultConfiguration,
        event_bus: EventBus,
        souc: SimulationObjectUpdatingComponent,
        interlocking_disruptor: IInterlockingDisruptor,
    ):
        return TrainPrioFault(
            configuration=train_prio_fault_configuration,
            event_bus=event_bus,
            simulation_object_updater=souc,
            interlocking_disruptor=interlocking_disruptor,
        )

    def test_inject_train_prio_fault(
        self,
        tick,
        train_prio_fault: TrainPrioFault,
        basic_train: Train,
    ):
        basic_train.train_type.priority = 1
        train_prio_fault.inject_fault(tick)
        assert (
            basic_train.train_type.priority == train_prio_fault.configuration.new_prio
        )
        assert (
            train_prio_fault.interlocking_disruptor.route_controller.method_calls == 1
        )

    def test_resolve_train_prio_fault(
        self,
        tick,
        train_prio_fault: TrainPrioFault,
        basic_train: Train,
    ):
        basic_train.train_type.priority = 5
        train_prio_fault.inject_fault(tick)
        assert (
            basic_train.train_type.priority == train_prio_fault.configuration.new_prio
        )
        assert (
            train_prio_fault.interlocking_disruptor.route_controller.method_calls == 1
        )
        train_prio_fault.resolve_fault(tick)
        assert basic_train.train_type.priority == train_prio_fault.old_prio == 5
        assert (
            train_prio_fault.interlocking_disruptor.route_controller.method_calls == 2
        )

    def test_resolve_train_not_in_simulation(
        self,
        tick,
        train_prio_fault: TrainPrioFault,
        basic_train: Train,
        souc: SimulationObjectUpdatingComponent,
    ):
        """tests that nothing happens when resolving the TrainPrioFault while
        the affected train is not in the simulation
        """

        train_prio_fault.train = basic_train
        train_prio_fault.old_prio = 3
        basic_train.train_type.priority = 5

        # remove train from sim
        souc.simulation_objects.remove(basic_train)

        assert (
            train_prio_fault.get_train_or_none(
                train_prio_fault.simulation_object_updater, basic_train.identifier
            )
            is None
        )
        train_prio_fault.resolve_fault(tick)
        assert basic_train.train_type.priority == 5
