import pytest
from traci import vehicle

from src.event_bus.event_bus import EventBus
from src.fault_injector.fault_configurations.train_speed_fault_configuration import (
    TrainSpeedFaultConfiguration,
)
from src.fault_injector.fault_types.train_speed_fault import TrainSpeedFault
from src.interlocking_component.route_controller import IInterlockingDisruptor
from src.wrapper.simulation_object_updating_component import (
    SimulationObjectUpdatingComponent,
)
from src.wrapper.simulation_objects import Train
from tests.decorators import recreate_db_setup

# pylint: disable=protected-access


class TestTrainSpeedFault:
    """Tests for TrainSpeedFault"""

    @recreate_db_setup
    def setup_method(self):
        pass

    @pytest.fixture
    def train_speed_fault_configuration(self, basic_train: Train):
        return TrainSpeedFaultConfiguration.create(
            **{
                "start_time": 40,
                "end_time": 400,
                "description": "test TrainSpeedFault",
                "affected_element_id": basic_train.identifier,
                "new_speed": 30,
                "strategy": "regular",
            }
        )

    @pytest.fixture
    def train_speed_fault(
        self,
        train_speed_fault_configuration: TrainSpeedFaultConfiguration,
        event_bus: EventBus,
        souc: SimulationObjectUpdatingComponent,
        interlocking_disruptor: IInterlockingDisruptor,
    ):
        return TrainSpeedFault(
            configuration=train_speed_fault_configuration,
            event_bus=event_bus,
            simulation_object_updater=souc,
            interlocking_disruptor=interlocking_disruptor,
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
        basic_train: Train,
        souc: SimulationObjectUpdatingComponent,
    ):
        basic_train.train_type.max_speed = 100
        train_speed_fault.inject_fault(tick=tick)
        assert (
            basic_train.train_type.max_speed
            == train_speed_fault.configuration.new_speed
        )
        # assert (
        #     train_speed_fault.interlocking_disruptor.route_controller.method_calls == 1
        # )

    def test_resolve_train_speed_fault(
        self,
        tick,
        train_speed_fault: TrainSpeedFault,
        basic_train: Train,
    ):
        basic_train.train_type.max_speed = 50
        train_speed_fault.inject_fault(tick=tick)
        assert (
            basic_train.train_type.max_speed
            == train_speed_fault.configuration.new_speed
        )
        # assert (
        #     train_speed_fault.interlocking_disruptor.route_controller.method_calls == 1
        # )
        train_speed_fault.resolve_fault(tick=tick)
        assert basic_train.train_type.max_speed == train_speed_fault.old_speed == 50
        # assert (
        #     train_speed_fault.interlocking_disruptor.route_controller.method_calls == 2
        # )

    def test_resolve_train_not_in_simulation(
        self,
        tick,
        train_speed_fault: TrainSpeedFault,
        basic_train: Train,
        souc: SimulationObjectUpdatingComponent,
    ):
        """tests that nothing happens when resolving the TrainSpeedFault
        while the affected train is not in the simulation
        """

        train_speed_fault.train = basic_train
        train_speed_fault.old_speed = 3
        basic_train.train_type._max_speed = 5

        # remove train from sim
        souc.simulation_objects.remove(basic_train)

        assert (
            train_speed_fault.get_train_or_none(
                train_speed_fault.simulation_object_updater, basic_train.identifier
            )
            is None
        )
        train_speed_fault.resolve_fault(tick)
        assert basic_train.train_type.max_speed == 5
