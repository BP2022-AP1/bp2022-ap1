from datetime import datetime

import pytest

from src.schedule.smard_api import SmardApi
from tests.decorators import recreate_db_setup


class TestSmardApi:
    """Test the SMARD API"""

    @recreate_db_setup
    def setup_method(self):
        pass

    @pytest.mark.usefixtures("demand_strategy_available_interval")
    def test_data_available(
        self, demand_strategy_available_interval: tuple[datetime, datetime]
    ):
        start, end = demand_strategy_available_interval
        availability = SmardApi().data_availability(start, end)
        assert availability.available
        assert not availability.interval_altered
        assert availability.start >= start
        assert availability.start <= end
        assert availability.end >= start
        assert availability.end <= end
        assert availability.start <= availability.end

    @pytest.mark.usefixtures("demand_strategy_not_available_interval")
    def test_no_data_available(
        self, demand_strategy_not_available_interval: tuple[datetime, datetime]
    ):
        start, end = demand_strategy_not_available_interval
        availability = SmardApi().data_availability(start, end)
        assert not availability.available

    @pytest.mark.usefixtures("demand_strategy_available_interval")
    def test_negative_length_interval(
        self, demand_strategy_available_interval: tuple[datetime, datetime]
    ):
        start, end = demand_strategy_available_interval
        availability = SmardApi().data_availability(end, start)
        assert not availability.available

    @pytest.mark.usefixtures("demand_strategy_available_interval")
    def test_get_data(
        self, demand_strategy_available_interval: tuple[datetime, datetime]
    ):
        start, end = demand_strategy_available_interval
        data = SmardApi().get_data(start, end)
        assert len(data) > 0
        assert data[0].timestamp >= start
        assert data[-1].timestamp <= end

    @pytest.mark.usefixtures("demand_strategy_not_available_interval")
    def test_dont_get_data(
        self, demand_strategy_not_available_interval: tuple[datetime, datetime]
    ):
        start, end = demand_strategy_not_available_interval
        data = SmardApi().get_data(start, end)
        assert len(data) == 0
