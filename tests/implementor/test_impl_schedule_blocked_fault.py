from uuid import UUID

from src import implementor as impl
from src.fault_injector.fault_configurations.schedule_blocked_fault_configuration import (
    ScheduleBlockedFaultConfiguration,
    ScheduleBlockedFaultConfigurationXSimulationConfiguration,
)


class TestScheduleBlockedFaultConfiguration:
    def test_get_all_schedule_blocked_fault_configuration_ids(
        self, token, schedule_blocked_fault_configuration_data
    ):
        config = ScheduleBlockedFaultConfiguration.create(
            **schedule_blocked_fault_configuration_data
        )

        response = impl.component.get_all_schedule_blocked_fault_configuration_ids(
            {}, token
        )
        (result, status) = response
        assert status == 200
        assert str(config.id) in result

    def test_get_all_schedule_blocked_fault_configuration_ids(
        self,
        token,
        schedule_blocked_fault_configuration_data,
        empty_simulation_configuration,
    ):
        config = ScheduleBlockedFaultConfiguration.create(
            **schedule_blocked_fault_configuration_data
        )
        another_config = ScheduleBlockedFaultConfiguration.create(
            **schedule_blocked_fault_configuration_data
        )
        ScheduleBlockedFaultConfigurationXSimulationConfiguration.create(
            simulation_configuration=empty_simulation_configuration,
            schedule_blocked_fault_configuration=config,
        )

        response = impl.component.get_all_schedule_blocked_fault_configuration_ids(
            {"simulationId": str(empty_simulation_configuration.id)}, token
        )
        (result, status) = response

        assert status == 200
        assert str(config.id) in result
        assert str(another_config.id) not in result

    def test_create_schedule_blocked_fault_configuration(
        token, schedule_blocked_fault_configuration_data
    ):
        def compare(a: object, b: object) -> bool:
            if isinstance(a, UUID) or isinstance(b, UUID):
                return str(a) == str(b)
            else:
                return a == b

        response = impl.component.create_schedule_blocked_fault_configuration(
            schedule_blocked_fault_configuration_data, token
        )
        (result, status) = response
        assert status == 201
        assert result["id"]
        configs = ScheduleBlockedFaultConfiguration.select().where(
            ScheduleBlockedFaultConfiguration.id == result["id"]
        )
        assert configs.exists()
        config = configs.get()
        for key in schedule_blocked_fault_configuration_data:
            assert compare(
                getattr(config, key), schedule_blocked_fault_configuration_data[key]
            )
