from src import implementor as impl
from src.fault_injector.fault_configurations.train_speed_fault_configuration import (
    TrainSpeedFaultConfiguration,
    TrainSpeedFaultConfigurationXSimulationConfiguration,
)


class TestRunImplementor:
    def test_get_all_train_speed_fault_configuration_ids(
        self, token, train_speed_fault_configuration_data
    ):
        config = TrainSpeedFaultConfiguration.create(
            **train_speed_fault_configuration_data
        )

        response = impl.component.get_all_train_speed_fault_configuration_ids(
            {}, token
        )
        (result, status) = response
        assert status == 200
        assert str(config.id) in result

    def test_get_all_train_speed_fault_configuration_ids(
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
        token, train_speed_fault_configuration_data
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
            assert (
                getattr(config, key) == train_speed_fault_configuration_data[key]
            )
