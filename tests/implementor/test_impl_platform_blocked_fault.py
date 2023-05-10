from src import implementor as impl
from src.fault_injector.fault_configurations.platform_blocked_fault_configuration import (
    PlatformBlockedFaultConfiguration,
    PlatformBlockedFaultConfigurationXSimulationConfiguration,
)


class TestPlatformBlockedFaultConfiguration:
    def test_get_all_platform_blocked_fault_configuration_ids(
        self, token, platform_blocked_fault_configuration_data
    ):
        config = PlatformBlockedFaultConfiguration.create(
            **platform_blocked_fault_configuration_data
        )

        response = impl.component.get_all_platform_blocked_fault_configuration_ids(
            {}, token
        )
        (result, status) = response
        assert status == 200
        assert str(config.id) in result

    def test_get_all_platform_blocked_fault_configuration_ids(
        self,
        token,
        platform_blocked_fault_configuration_data,
        empty_simulation_configuration,
    ):
        config = PlatformBlockedFaultConfiguration.create(
            **platform_blocked_fault_configuration_data
        )
        another_config = PlatformBlockedFaultConfiguration.create(
            **platform_blocked_fault_configuration_data
        )
        PlatformBlockedFaultConfigurationXSimulationConfiguration.create(
            simulation_configuration=empty_simulation_configuration,
            platform_blocked_fault_configuration=config,
        )

        response = impl.component.get_all_platform_blocked_fault_configuration_ids(
            {"simulationId": str(empty_simulation_configuration.id)}, token
        )
        (result, status) = response

        assert status == 200
        assert str(config.id) in result
        assert str(another_config.id) not in result

    def test_create_platform_blocked_fault_configuration(
        token, platform_blocked_fault_configuration_data
    ):
        response = impl.component.create_platform_blocked_fault_configuration(
            platform_blocked_fault_configuration_data, token
        )
        (result, status) = response
        assert status == 201
        assert result["id"]
        configs = PlatformBlockedFaultConfiguration.select().where(
            PlatformBlockedFaultConfiguration.id == result["id"]
        )
        assert configs.exists()
        config = configs.get()
        for key in platform_blocked_fault_configuration_data:
            assert (
                getattr(config, key) == platform_blocked_fault_configuration_data[key]
            )