# pylint: disable=unused-argument
# pylint: disable=duplicate-code

import json

from src.communicator.communicator import Communicator
from src.event_bus.event_bus import EventBus
from src.fault_injector.fault_types.platform_blocked_fault import PlatformBlockedFault
from src.fault_injector.fault_types.schedule_blocked_fault import ScheduleBlockedFault
from src.fault_injector.fault_types.track_blocked_fault import TrackBlockedFault
from src.fault_injector.fault_types.track_speed_limit_fault import TrackSpeedLimitFault
from src.fault_injector.fault_types.train_prio_fault import TrainPrioFault
from src.fault_injector.fault_types.train_speed_fault import TrainSpeedFault
from src.implementor.models import Run, SimulationConfiguration, Token
from src.interlocking_component.route_controller import (
    IInterlockingDisruptor,
    RouteController,
)
from src.logger.logger import Logger
from src.spawner.spawner import Spawner
from src.wrapper.simulation_object_updating_component import (
    SimulationObjectUpdatingComponent,
)
from src.wrapper.train_builder import TrainBuilder


def get_all_run_ids(options: dict, token: Token):
    """
    :param options: A dictionary containing all the paramters for the Operations
        options["simulationId"]
    :param token: Token object of the current user

    """

    # Return all runs of a single simulation configuration
    simulation_configuration_key = "simulationId"
    if (
        simulation_configuration_key in options
        and options[simulation_configuration_key] is not None
    ):
        simulation_id = options[simulation_configuration_key]
        simulation_configurations = SimulationConfiguration.select().where(
            SimulationConfiguration.id == simulation_id
        )

        if not simulation_configurations.exists():
            return "Simulation not found", 404

        simulation_configuration = simulation_configurations.get()
        runs = simulation_configuration.runs

        runs_string = [str(run.id) for run in runs]
        return runs_string, 200

    runs = [str(run.id) for run in Run.select()]
    return runs, 200


# Can't reduce the number of local variables here, because we have many components
# pylint: disable=too-many-locals
def create_run(body, token):
    """

    :param body: The parsed body of the request
    :param token: Token object of the current user
    """
    simulation_configuration_id = body.pop("simulation_configuration")
    simulation_configurations = SimulationConfiguration.select().where(
        SimulationConfiguration.id == simulation_configuration_id
    )
    if not simulation_configurations.exists():
        return "Simulation not found", 404

    simulation_configuration = simulation_configurations.get()
    communicator = Communicator()

    run = Run(simulation_configuration=simulation_configuration)
    run.save()
    event_bus = EventBus(run_id=run.id)
    logger = Logger(run_id=run.id, event_bus=event_bus)
    communicator.add_component(logger)

    object_updater = SimulationObjectUpdatingComponent(event_bus)
    communicator.add_component(object_updater)

    # if simulation_configuration.interlocking_configuration_references.exists():
    #    references = (
    #        simulation_configuration.interlocking_configuration_references.get()
    #    )
    #    reference = references.interlocking_configuration.get()
    #    interlocking_configuration = reference.interlocking_component
    #    interlocking_component = RouteController(event_bus, interlocking_configuration)
    #    communicator.add_component(interlocking_component)

    route_controller = RouteController(event_bus, 1, object_updater)
    communicator.add_component(route_controller)

    # The todo will be replaces in other PR when the interlocking component is implemented
    # pylint: disable=fixme
    # TODO: get real interlocking disruptor
    interlocking_disruptor: IInterlockingDisruptor = None
    # pylint: enable=fixme

    train_spawner = TrainBuilder(object_updater, route_controller)

    if simulation_configuration.spawner_configuration_references.exists():
        reference = simulation_configuration.spawner_configuration_references.get()
        spawner_config = reference.spawner_configuration
        spawner = Spawner(
            configuration=spawner_config,
            event_bus=event_bus,
            train_spawner=train_spawner,
        )
        communicator.add_component(spawner)

    for (
        reference
    ) in simulation_configuration.platform_blocked_fault_configuration_references:
        platform_blocked_fault_config = reference.platform_blocked_fault_configuration
        fault = PlatformBlockedFault(
            platform_blocked_fault_config,
            event_bus,
            object_updater,
            interlocking_disruptor,
        )
        communicator.add_component(fault)

    for (
        reference
    ) in simulation_configuration.schedule_blocked_fault_configuration_references:
        schedule_blocked_fault_config = reference.schedule_blocked_fault_configuration
        fault = ScheduleBlockedFault(
            schedule_blocked_fault_config,
            event_bus,
            object_updater,
            interlocking_disruptor,
            spawner,
        )
        communicator.add_component(fault)

    for (
        reference
    ) in simulation_configuration.track_blocked_fault_configuration_references:
        track_blocked_fault_config = reference.track_blocked_fault_configuration
        fault = TrackBlockedFault(
            track_blocked_fault_config,
            event_bus,
            object_updater,
            interlocking_disruptor,
        )
        communicator.add_component(fault)

    for (
        reference
    ) in simulation_configuration.track_speed_limit_fault_configuration_references:
        track_speed_limit_fault_config = reference.track_speed_limit_fault_configuration
        fault = TrackSpeedLimitFault(
            track_speed_limit_fault_config,
            event_bus,
            object_updater,
            interlocking_disruptor,
        )
        communicator.add_component(fault)

    for (
        reference
    ) in simulation_configuration.train_speed_fault_configuration_references:
        train_speed_fault_config = reference.train_speed_fault_configuration
        fault = TrainSpeedFault(
            train_speed_fault_config,
            event_bus,
            object_updater,
            interlocking_disruptor,
        )
        communicator.add_component(fault)

    for reference in simulation_configuration.train_prio_fault_configuration_references:
        train_prio_fault_config = reference.train_prio_fault_configuration
        fault = TrainPrioFault(
            train_prio_fault_config,
            event_bus,
            object_updater,
            interlocking_disruptor,
        )
        communicator.add_component(fault)

    process_id = communicator.run()

    Run.update({Run.process_id: process_id}).where(Run.id == run.id).execute()

    return (
        {
            "id": str(run.id),
        },
        201,
    )


# pylint: enable=too-many-locals


def get_run(options, token):
    """
    :param options: A dictionary containing all the paramters for the Operations
        options["id"]
    :param token: Token object of the current user

    """

    # Implement your business logic here
    # All the parameters are present in the options argument

    return json.dumps("<map>"), 501  # 200


def delete_run(options, token):
    """
    :param options: A dictionary containing all the paramters for the Operations
        options["id"]
    :param token: Token object of the current user

    """

    # Implement your business logic here
    # All the parameters are present in the options argument

    return "", 501  # 204
