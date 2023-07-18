import pytest

from src import implementor as impl
from src.schedule.schedule_configuration import ScheduleConfiguration
from src.spawner.spawner import SpawnerConfiguration, SpawnerConfigurationXSchedule


# pylint: disable=duplicate-code
class TestScheduleConfiguration:
    """
    Tests for correct functionality of schedule configuration endpoint
    if the input data is valid.
    """

    @pytest.mark.parametrize(
        "strategy, configuration_fixture, not_found_configuration_fixture",
        [
            (
                "RegularScheduleStrategy",
                "regular_train_schedule_configuration",
                "random_train_schedule_configuration",
            ),
            (
                "RandomScheduleStrategy",
                "random_train_schedule_configuration",
                "demand_train_schedule_configuration",
            ),
            (
                "DemandScheduleStrategy",
                "demand_train_schedule_configuration",
                "regular_train_schedule_configuration",
            ),
        ],
    )
    def test_get_all_schedule_configuration_ids(
        self,
        token,
        strategy,
        configuration_fixture,
        not_found_configuration_fixture,
        request: pytest.FixtureRequest,
    ):
        configuration = request.getfixturevalue(configuration_fixture)
        not_found_configuration = request.getfixturevalue(
            not_found_configuration_fixture
        )

        (result, status) = impl.schedule.get_all_schedule_ids(
            {"strategy": strategy}, token
        )
        assert status == 200
        assert str(configuration.id) in result
        assert str(not_found_configuration.id) not in result

    @pytest.mark.parametrize(
        "configuration_data_fixture",
        [
            "regular_train_schedule_data",
            "random_train_schedule_data",
            "demand_train_schedule_data",
        ],
    )
    def test_create_schedule_configuration(
        self,
        token,
        configuration_data_fixture,
        platform_ids,
        request: pytest.FixtureRequest,
    ):
        configuration_data = request.getfixturevalue(configuration_data_fixture)
        strategy = configuration_data.pop("strategy_type")
        configuration_data["platforms"] = platform_ids
        (result, status) = impl.schedule.create_schedule(
            configuration_data, {"strategy": strategy}, token
        )
        assert status == 201
        assert result["id"] is not None
        config = ScheduleConfiguration.get_by_id(result["id"])
        assert config is not None
        assert config.strategy_type == strategy
        for key, value in configuration_data.items():
            assert getattr(config, key) == value
        platform_reference = list(config.train_schedule_platform_references)
        for reference in platform_reference:
            platform_id = platform_ids[reference.index]
            assert platform_id == reference.simulation_platform_id

    @pytest.mark.parametrize(
        "configuration_data_fixture, configuration_fixture",
        [
            ("regular_train_schedule_data", "regular_train_schedule_configuration"),
            ("random_train_schedule_data", "random_train_schedule_configuration"),
            ("demand_train_schedule_data", "demand_train_schedule_configuration"),
        ],
    )
    def test_get_single_schedule_configuration(
        self,
        token,
        configuration_data_fixture,
        configuration_fixture,
        platform_ids,
        request: pytest.FixtureRequest,
    ):
        configuration_data = request.getfixturevalue(configuration_data_fixture)
        configuration = request.getfixturevalue(configuration_fixture)
        strategy = configuration_data.pop("strategy_type")

        (result, status) = impl.schedule.get_schedule(
            {"strategy": strategy, "identifier": str(configuration.id)}, token
        )
        assert status == 200
        configuration_data["strategy_type"] = strategy
        for key, item in configuration_data.items():
            assert result[key] == item

        for index, platform in enumerate(result["platforms"]):
            assert platform == platform_ids[index]

    @pytest.mark.parametrize(
        "strategy",
        [
            "RegularScheduleStrategy",
            "RandomScheduleStrategy",
            "DemandScheduleStrategy",
        ],
    )
    def test_get_single_schedule_configuration_not_found(self, token, strategy):
        (result, status) = impl.schedule.get_schedule(
            {
                "strategy": strategy,
                "identifier": "00000000-0000-0000-0000-000000000000",
            },
            token,
        )
        assert status == 404
        assert result == "Schedule not found"

    @pytest.mark.parametrize(
        "strategy, configuration_fixture",
        [
            ("RegularScheduleStrategy", "regular_train_schedule_configuration"),
            ("RandomScheduleStrategy", "random_train_schedule_configuration"),
            ("DemandScheduleStrategy", "demand_train_schedule_configuration"),
        ],
    )
    def test_delete_schedule_configuration(
        self, token, strategy, configuration_fixture, request: pytest.FixtureRequest
    ):
        configuration = request.getfixturevalue(configuration_fixture)
        (result, status) = impl.schedule.delete_schedule(
            {"strategy": strategy, "identifier": str(configuration.id)}, token
        )
        assert status == 204
        assert result == "Schedule deleted"
        configs = ScheduleConfiguration.select().where(
            ScheduleConfiguration.id == configuration.id
        )
        assert not configs.exists()

    @pytest.mark.parametrize(
        "strategy",
        [
            "RegularScheduleStrategy",
            "RandomScheduleStrategy",
            "DemandScheduleStrategy",
        ],
    )
    def test_delete_schedule_configuration_not_found(self, strategy, token):
        (result, status) = impl.schedule.delete_schedule(
            {
                "strategy": strategy,
                "identifier": "00000000-0000-0000-0000-000000000000",
            },
            token,
        )
        assert status == 404
        assert result == "Schedule not found"

    @pytest.mark.parametrize(
        "strategy, configuration_fixture",
        [
            ("RegularScheduleStrategy", "regular_train_schedule_configuration"),
            ("RandomScheduleStrategy", "random_train_schedule_configuration"),
            ("DemandScheduleStrategy", "demand_train_schedule_configuration"),
        ],
    )
    def test_delete_schedule_configuration_in_use(
        self, strategy, configuration_fixture, token, request: pytest.FixtureRequest
    ):
        configuration = request.getfixturevalue(configuration_fixture)
        spawner = SpawnerConfiguration()
        spawner.save()
        SpawnerConfigurationXSchedule(
            spawner_configuration_id=spawner,
            schedule_configuration_id=configuration,
        ).save()
        (result, status) = impl.schedule.delete_schedule(
            {"strategy": strategy, "identifier": str(configuration.id)}, token
        )

        assert status == 400
        assert (
            result == "Schedule configuration is referenced by a spawner configuration"
        )
