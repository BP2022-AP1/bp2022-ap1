import uuid

from src import implementor as impl
from src.fault_injector.fault_configurations.track_speed_limit_fault_configuration import (
    TrackSpeedLimitFaultConfiguration,
    TrackSpeedLimitFaultConfigurationXSimulationConfiguration,
)


class TestTrackSpeedLimitFaultConfiguration:
    """Test for TrackSpeedLimitFaultConfiguration"""

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

    def test_get_all_track_speed_limit_fault_configuration_ids2(
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
        self, token, track_speed_limit_fault_configuration_data
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

    def test_get_track_speed_limit_fault_configuration(
        self, token, track_speed_limit_fault_configuration_data
    ):
        config = TrackSpeedLimitFaultConfiguration.create(
            **track_speed_limit_fault_configuration_data
        )

        response = impl.component.get_track_speed_limit_fault_configuration(
            {"identifier": str(config.id)}, token
        )
        (result, status) = response
        assert status == 200
        assert str(config.id) == result["id"]
        assert str(config.updated_at) == result["updated_at"]
        assert str(config.created_at) == result["created_at"]
        assert config.start_time == result["start_time"]
        assert str(config.readable_id) == result["readable_id"]
        assert config.end_time == result["end_time"]
        assert config.inject_probability == result["inject_probability"]
        assert config.resolve_probability == result["resolve_probability"]
        assert str(config.description) == result["description"]
        assert str(config.strategy) == result["strategy"]
        assert str(config.affected_element_id) == result["affected_element_id"]

    def test_delete_track_speed_limit_fault_configuration(
        self,
        token,
        track_speed_limit_fault_configuration_data,
    ):
        config = TrackSpeedLimitFaultConfiguration.create(
            **track_speed_limit_fault_configuration_data
        )
        response = impl.component.delete_track_speed_limit_fault_configuration(
            {"identifier": str(config.id)}, token
        )
        (result, status) = response
        assert status == 204
        assert result == "Deleted track-speed-limit-fault configuration"
        assert (
            not TrackSpeedLimitFaultConfiguration.select()
            .where(TrackSpeedLimitFaultConfiguration.id == config.id)
            .exists()
        )

    # pylint: disable=unused-argument

    def test_delete_track_speed_limit_fault_configuration_not_found(
        self,
        token,
        track_speed_limit_fault_configuration_data,
    ):
        object_id = uuid.uuid4()
        response = impl.component.delete_track_speed_limit_fault_configuration(
            {"identifier": object_id}, token
        )
        (result, status) = response
        assert status == 404
        assert result == "Id not found"

    def test_delete_track_speed_limit_fault_configuration_in_use(
        self,
        token,
        track_speed_limit_fault_configuration_data,
        empty_simulation_configuration,
    ):
        config = TrackSpeedLimitFaultConfiguration.create(
            **track_speed_limit_fault_configuration_data
        )
        TrackSpeedLimitFaultConfigurationXSimulationConfiguration.create(
            simulation_configuration=empty_simulation_configuration,
            track_speed_limit_fault_configuration=config,
        )
        response = impl.component.delete_track_speed_limit_fault_configuration(
            {"identifier": str(config.id)}, token
        )
        (result, status) = response
        assert status == 400
        assert (
            result
            == "Track speed limit fault configuration is referenced by a simulation configuration"
        )
