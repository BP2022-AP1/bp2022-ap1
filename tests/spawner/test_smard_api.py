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
        availabilities = SmardApi().data_availability(start, end)
        assert availabilities.available
        assert not availabilities.interval_altered
        assert availabilities.start >= start
        assert availabilities.start <= end
        assert availabilities.end >= start
        assert availabilities.end <= end
        assert availabilities.start <= availabilities.end

    @pytest.mark.usefixtures("demand_strategy_not_available_interval")
    def test_no_data_available(
        self, demand_strategy_not_available_interval: tuple[datetime, datetime]
    ):
        start, end = demand_strategy_not_available_interval
        availabilities = SmardApi().data_availability(start, end)
        assert not availabilities.available
        assert not availabilities.interval_altered
        assert availabilities.start is None
        assert availabilities.end is None

    @pytest.mark.usefixtures("demand_strategy_available_interval")
    def test_get_data(
        self, demand_strategy_available_interval: tuple[datetime, datetime]
    ):
        start, end = demand_strategy_available_interval
        data = SmardApi().get_data(start, end)
        assert len(data) > 0
        assert data[0].timestamp >= start
        assert data[-1].timestamp <= end
