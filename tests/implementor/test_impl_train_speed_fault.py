import uuid

from src import implementor as impl
from src.fault_injector.fault_configurations.train_speed_fault_configuration import (
    TrainSpeedFaultConfiguration,
    TrainSpeedFaultConfigurationXSimulationConfiguration,
)


# pylint: disable=duplicate-code
class TestTrainSpeedFaultConfiguration:
    """
    Tests for correct functionality of train speed fault configuration endpoint
    if the input data is valid.
    """

    def test_get_all_train_speed_fault_configuration_ids(
        self, token, train_speed_fault_configuration_data
    ):
        config = TrainSpeedFaultConfiguration.create(
            **train_speed_fault_configuration_data
        )

        response = impl.component.get_all_train_speed_fault_configuration_ids({}, token)
        (result, status) = response
        assert status == 200
        assert str(config.id) in result

    def test_get_all_train_speed_fault_configuration_ids_with_simulation(
        self,
        token,
        train_speed_fault_configuration_data,
        empty_simulation_configuration,
    ):
        config = TrainSpeedFaultConfiguration.create(
            **train_speed_fault_configuration_data
        )
        another_config = TrainSpeedFaultConfiguration.create(
            **train_speed_fault_configuration_data
        )
        TrainSpeedFaultConfigurationXSimulationConfiguration.create(
            simulation_configuration=empty_simulation_configuration,
            train_speed_fault_configuration=config,
        )

        response = impl.component.get_all_train_speed_fault_configuration_ids(
            {"simulationId": str(empty_simulation_configuration.id)}, token
        )
        (result, status) = response

        assert status == 200
        assert str(config.id) in result
        assert str(another_config.id) not in result

    def test_create_train_speed_fault_configuration(
        self, token, train_speed_fault_configuration_data
    ):
        response = impl.component.create_train_speed_fault_configuration(
            train_speed_fault_configuration_data, token
        )
        (result, status) = response
        assert status == 201
        assert result["id"]
        configs = TrainSpeedFaultConfiguration.select().where(
            TrainSpeedFaultConfiguration.id == result["id"]
        )
        assert configs.exists()
        config = configs.get()
        for key in train_speed_fault_configuration_data:
            assert getattr(config, key) == train_speed_fault_configuration_data[key]

    def test_get_train_speed_fault_configuration(
        self, token, train_speed_fault_configuration_data
    ):
        config = TrainSpeedFaultConfiguration.create(
            **train_speed_fault_configuration_data
        )

        response = impl.component.get_train_speed_fault_configuration(
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

    def test_delete_train_speed_fault_configuration(
        self,
        token,
        train_speed_fault_configuration_data,
    ):
        config = TrainSpeedFaultConfiguration.create(
            **train_speed_fault_configuration_data
        )
        response = impl.component.delete_train_speed_fault_configuration(
            {"identifier": str(config.id)}, token
        )
        (result, status) = response
        assert status == 204
        assert result == "Deleted train-speed-fault configuration"
        assert (
            not TrainSpeedFaultConfiguration.select()
            .where(TrainSpeedFaultConfiguration.id == config.id)
            .exists()
        )

    def test_delete_train_speed_fault_configuration_not_found(
        self,
        token,
    ):
        object_id = uuid.uuid4()
        response = impl.component.delete_train_speed_fault_configuration(
            {"identifier": object_id}, token
        )
        (result, status) = response
        assert status == 404
        assert result == "Id not found"

    def test_delete_train_speed_fault_configuration_in_use(
        self,
        token,
        train_speed_fault_configuration_data,
        empty_simulation_configuration,
    ):
        config = TrainSpeedFaultConfiguration.create(
            **train_speed_fault_configuration_data
        )
        TrainSpeedFaultConfigurationXSimulationConfiguration.create(
            simulation_configuration=empty_simulation_configuration,
            train_speed_fault_configuration=config,
        )
        response = impl.component.delete_train_speed_fault_configuration(
            {"identifier": str(config.id)}, token
        )
        (result, status) = response
        assert status == 400
        assert (
            result
            == "Train speed fault configuration is referenced by a simulation configuration"
        )
