import uuid
from uuid import UUID

from src import implementor as impl
from src.fault_injector.fault_configurations.schedule_blocked_fault_configuration import (
    ScheduleBlockedFaultConfiguration,
    ScheduleBlockedFaultConfigurationXSimulationConfiguration,
)


# pylint: disable=duplicate-code
class TestScheduleBlockedFaultConfiguration:
    """
    Tests for correct functionality of schedule blocked fault configuration endpoint
    if the input data is valid.
    """

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

    def test_get_all_schedule_blocked_fault_configuration_ids_with_simulation(
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
        self, token, schedule_blocked_fault_configuration_data
    ):
        def compare(first: object, second: object) -> bool:
            if isinstance(first, UUID) or isinstance(second, UUID):
                return str(first) == str(second)
            return first == second

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

    def test_get_schedule_blocked_fault_configuration(
        self, token, schedule_blocked_fault_configuration_data
    ):
        config = ScheduleBlockedFaultConfiguration.create(
            **schedule_blocked_fault_configuration_data
        )

        response = impl.component.get_schedule_blocked_fault_configuration(
            {"identifier": str(config.id)}, token
        )
        (result, status) = response
        assert status == 200
        assert str(config.id) == result["id"]
        assert str(config.updated_at) == result["updated_at"]
        assert str(config.created_at) == result["created_at"]
        assert str(config.readable_id) == result["readable_id"]
        assert config.start_time == result["start_time"]
        assert config.end_time == result["end_time"]
        assert config.inject_probability == result["inject_probability"]
        assert config.resolve_probability == result["resolve_probability"]
        assert str(config.description) == result["description"]
        assert str(config.strategy) == result["strategy"]
        assert str(config.affected_element_id) == result["affected_element_id"]

    def test_delete_schedule_blocked_fault_configuration(
        self,
        token,
        schedule_blocked_fault_configuration_data,
    ):
        config = ScheduleBlockedFaultConfiguration.create(
            **schedule_blocked_fault_configuration_data
        )
        response = impl.component.delete_schedule_blocked_fault_configuration(
            {"identifier": str(config.id)}, token
        )
        (result, status) = response
        assert status == 204
        assert result == "Deleted schedule-blocked-fault configuration"
        assert (
            not ScheduleBlockedFaultConfiguration.select()
            .where(ScheduleBlockedFaultConfiguration.id == config.id)
            .exists()
        )

    def test_delete_schedule_blocked_fault_configuration_not_found(
        self,
        token,
    ):
        object_id = uuid.uuid4()
        response = impl.component.delete_schedule_blocked_fault_configuration(
            {"identifier": object_id}, token
        )
        (result, status) = response
        assert status == 404
        assert result == "Id not found"

    def test_delete_schedule_blocked_fault_configuration_in_use(
        self,
        token,
        schedule_blocked_fault_configuration_data,
        empty_simulation_configuration,
    ):
        config = ScheduleBlockedFaultConfiguration.create(
            **schedule_blocked_fault_configuration_data
        )
        ScheduleBlockedFaultConfigurationXSimulationConfiguration.create(
            simulation_configuration=empty_simulation_configuration,
            schedule_blocked_fault_configuration=config,
        )
        response = impl.component.delete_schedule_blocked_fault_configuration(
            {"identifier": str(config.id)}, token
        )
        (result, status) = response
        assert status == 400
        assert (
            result
            == "Schedule blocked fault configuration is referenced by a simulation configuration"
        )
