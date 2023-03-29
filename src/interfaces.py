from typing import Any, Protocol


class IComponent(Protocol):
    logger: "ILogger"
    priority: int

    def next_tick(self, tick: int, callback_object: Any):
        ...


class ISpawner(IComponent, Protocol):
    config: "SpawnerConfig"

    def add_schedule(self, schedule: "ISchedule") -> int:
        ...

    def remove_schedule(self, schedule_id: int):
        ...

    @property
    def schedules(self) -> list["ISchedule"]:
        ...
