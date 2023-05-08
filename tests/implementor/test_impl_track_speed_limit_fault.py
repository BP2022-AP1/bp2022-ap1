from src import implementor as impl
from src.fault_injector.fault_configurations.track_speed_limit_fault_configuration import (
    TrackSpeedLimitFaultConfiguration,
    TrackSpeedLimitFaultConfigurationXSimulationConfiguration,
)


class TestRunImplementor:
    def test_get_all_track_speed_limit_fault_configuration_ids(
        self, token, track_speed_limit_fault_configuration_data
    ):
        config = TrackSpeedLimitFaultConfiguration.create(
            **track_speed_limit_fault_configuration_data
        )

        response = impl.component.get_all_track_speed_limit_fault_configuration_ids(
            {}, token
        )
        (result, status) = response
        assert status == 200
        assert str(config.id) in result

    def test_get_all_track_speed_limit_fault_configuration_ids(
        self,
        token,
        track_speed_limit_fault_configuration_data,
        empty_simulation_configuration,
    ):
        config = TrackSpeedLimitFaultConfiguration.create(
            **track_speed_limit_fault_configuration_data
        )
        another_config = TrackSpeedLimitFaultConfiguration.create(
            **track_speed_limit_fault_configuration_data
        )
        TrackSpeedLimitFaultConfigurationXSimulationConfiguration.create(
            simulation_configuration=empty_simulation_configuration,
            track_speed_limit_fault_configuration=config,
        )

        response = impl.component.get_all_track_speed_limit_fault_configuration_ids(
            {"simulationId": str(empty_simulation_configuration.id)}, token
        )
        (result, status) = response

        assert status == 200
        assert str(config.id) in result
        assert str(another_config.id) not in result

    def test_create_track_speed_limit_fault_configuration(
        token, track_speed_limit_fault_configuration_data
    ):
        response = impl.component.create_track_speed_limit_fault_configuration(
            track_speed_limit_fault_configuration_data, token
        )
        (result, status) = response
        assert status == 201
        assert result["id"]
        configs = TrackSpeedLimitFaultConfiguration.select().where(
            TrackSpeedLimitFaultConfiguration.id == result["id"]
        )
        assert configs.exists()
        config = configs.get()
        for key in track_speed_limit_fault_configuration_data:
            assert (
                getattr(config, key) == track_speed_limit_fault_configuration_data[key]
            )
