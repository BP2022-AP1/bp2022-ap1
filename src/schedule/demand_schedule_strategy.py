from datetime import datetime, timedelta

from src.schedule.schedule_configuration import ScheduleConfiguration
from src.schedule.schedule_strategy import ScheduleStrategy
from src.schedule.smard_api import SmardApi


class DemandScheduleStrategy(ScheduleStrategy):
    """A schedule strategy that spawns trains based on the demand of coal
    for electricity production.
    """

    @classmethod
    def from_schedule_configuration(cls, schedule_configuration: ScheduleConfiguration):
        """Creates a new instance of this class from a schedule configuration.

        :param schedule_configuration: The schedule configuration to create the instance from.
        :return: The new instance.
        """
        assert schedule_configuration.strategy_type == "DemandScheduleStrategy"
        return cls(
            start_time=schedule_configuration.strategy_start_time,
            end_time=schedule_configuration.strategy_end_time,
            power_station=schedule_configuration.demand_strategy_power_station,
            scaling_factor=schedule_configuration.demand_strategy_scaling_factor,
            start_datetime=schedule_configuration.demand_strategy_start_datetime,
        )

    TOTAL_ELECTRICAL_POWER: float = 10632.75  # in MW
    # [see result from research/coal_consumption/coal_consumption.ipynb section 46]

    COAL_ENERGY_CONTENT: float = 5.56  # in MWh/t (= 20 MJ/kg)
    # [source: https://www.energie-lexikon.info/kohle.html]

    SECONDS_PER_QUARTER_HOUR: int = (60 / 4) * 60
    COAL_PER_WAGGON: float = 60  # in tons [source: interview]
    WAGGONS_PER_TRAIN: int = 16
    COAL_PER_TRAIN: float = COAL_PER_WAGGON * WAGGONS_PER_TRAIN  # in tons
    POWER_STATIONS: dict[str, dict[str, float]] = {
        "jaenschwalde": {
            "electrical_power": 3000.0,  # in MW
            "thermal_power": 349.0,  # in MW
            "efficiency": 0.355,
        },
        "boxberg": {
            "electrical_power": 2582.0,  # in MW
            "thermal_power": 125.0,  # in MW
            "efficiency": 0.42,
        },
        "schwarze_pumpe": {
            "electrical_power": 1600.0,  # in MW
            "thermal_power": 120.0,  # in MW
            "efficiency": 0.4,
        },
    }

    power_station: str
    scaling_factor: float
    start_datetime: datetime
    spawn_seconds: list[int]
    _api: SmardApi

    def __init__(
        self,
        start_time: int,
        end_time: int,
        power_station: str,
        scaling_factor: float,
        start_datetime: datetime,
    ):
        """Creates a new instance of this class.

        :param start_time: The time in seconds at which the schedule strategy starts.
        :param end_time: The time in seconds at which the schedule strategy ends.
        :param power_station: The power station to use for the calculation.
        :param scaling_factor: The scaling factor to multiply the coal consumption with.
        :param start_datetime: The start datetime for the used data.
        """
        super().__init__(start_time, end_time)
        self.power_station = power_station
        self.scaling_factor = scaling_factor
        self.start_datetime = start_datetime
        self.spawn_seconds = []
        self._api = SmardApi()
        self._calculate_spawn_seconds()

    def compute_coal_consumption(self, produced_electrical_energy: float) -> float:
        """Computes the coal consumption for the given amount of electrical energy
        for the given power station multiplied by the scaling factor.

        :param produced_electrical_energy: The amount of electrical energy produced.
        :return: The coal consumption.
        """
        max_electrical_power = self.POWER_STATIONS[self.power_station][
            "electrical_power"
        ]
        max_thermal_power = self.POWER_STATIONS[self.power_station]["thermal_power"]
        efficiency = self.POWER_STATIONS[self.power_station]["efficiency"]
        # the time in hours all stations on the grid have to run to produce
        # the given amount of electrical energy
        time = produced_electrical_energy / self.TOTAL_ELECTRICAL_POWER  # hours
        # that was copilot, exactly the formula I developed on my whiteboard... impressive
        coal_mass = (
            time
            * (max_electrical_power + max_thermal_power)
            / (self.COAL_ENERGY_CONTENT * efficiency)
        )
        return coal_mass * self.scaling_factor  # tons

    def _compute_trains_to_spawn(self, produced_electrical_power: float) -> float:
        """Computes the amount of trains to spawn for the given amount of electrical power.

        :param produced_electrical_power: The amount of electrical power produced.
        :return: The amount of trains to spawn.
        """
        coal_consumption = self.compute_coal_consumption(produced_electrical_power)
        return coal_consumption / self.COAL_PER_TRAIN

    def _calculate_spawn_seconds(self):
        """Calculates the ticks at which trains should spawn."""
        end_datetime = self.start_datetime + timedelta(
            seconds=self.end_time - self.start_time
        )
        data = self._api.get_data(self.start_datetime, end_datetime)
        train_accumulator = 0.0
        for quarter_hour, entry in enumerate(data):
            train_accumulator += self._compute_trains_to_spawn(entry.value)
            second = int(quarter_hour * self.SECONDS_PER_QUARTER_HOUR + self.start_time)
            while train_accumulator >= 1.0:
                self.spawn_seconds.append(second)
                train_accumulator -= 1.0
                second += 1

    def should_spawn(self, seconds: int) -> bool:
        """Returns whether a train should spawn at the given tick."""
        return super().should_spawn(seconds) and seconds in self.spawn_seconds
