from flask import Blueprint, request
from webargs.flaskparser import parser

from .. import implementor as impl
from ..schemas import model

bp = Blueprint("component", __name__)


@bp.route("/component/fault-injection/schedule-blocked-fault", methods=["get"])
def get_schedule_blocked_fault_configuration_ids():
    """Get all schedule blocked fault configuration ids"""
    options = {}
    options["simulationId"] = request.args.get("simulationId")

    return impl.component.get_schedule_blocked_fault_configuration_ids(options)


@bp.route("/component/fault-injection/schedule-blocked-fault", methods=["post"])
def create_schedule_blocked_fault_configuration():
    """Create a schedule blocked fault configuration"""
    schema = model.ScheduleBlockedFaultConfiguration()

    body = parser.parse(schema, request, location="json")

    return impl.component.create_schedule_blocked_fault_configuration(body)


@bp.route(
    "/component/fault-injection/schedule-blockedfault/<identifier>", methods=["get"]
)
def get_schedule_blocked_fault_configuration(identifier):
    """Get a schedule blocked fault configuration"""
    options = {}
    options["identifier"] = identifier

    return impl.component.get_schedule_blocked_fault_configuration(options)


@bp.route(
    "/component/fault-injection/schedule-blockedfault/<identifier>", methods=["put"]
)
def update_schedule_blocked_fault_configuration(identifier):
    """Update a schedule blocked fault configuration"""
    options = {}
    options["identifier"] = identifier

    schema = model.ScheduleBlockedFaultConfiguration()

    body = parser.parse(schema, request, location="json")

    return impl.component.update_schedule_blocked_fault_configuration(options, body)


@bp.route(
    "/component/fault-injection/schedule-blockedfault/<identifier>", methods=["delete"]
)
def delete_schedule_blocked_fault_configuration(identifier):
    """Delete a schedule blocked fault configuration"""
    options = {}
    options["identifier"] = identifier

    return impl.component.delete_schedule_blocked_fault_configuration(options)


@bp.route("/component/fault-injection/track-blocked-fault", methods=["get"])
def get_track_blocked_fault_configuration_ids():
    """Get all track blocked fault configuration ids"""
    options = {}
    options["simulationId"] = request.args.get("simulationId")

    return impl.component.get_track_blocked_fault_configuration_ids(options)


@bp.route("/component/fault-injection/track-blocked-fault", methods=["post"])
def create_track_blocked_fault_configuration():
    """Create a track blocked fault configuration"""
    schema = model.TrackBlockedFaultConfiguration()

    body = parser.parse(schema, request, location="json")

    return impl.component.create_track_blocked_fault_configuration(body)


@bp.route(
    "/component/fault-injection/track-blocked-fault/<identifier>", methods=["get"]
)
def get_track_blocked_fault_configuration(identifier):
    """Get a track blocked fault configuration"""
    options = {}
    options["identifier"] = identifier

    return impl.component.get_track_blocked_fault_configuration(options)


@bp.route(
    "/component/fault-injection/track-blocked-fault/<identifier>", methods=["put"]
)
def update_track_blocked_fault_configuration(identifier):
    """Update a track blocked fault configuration"""
    options = {}
    options["identifier"] = identifier

    schema = model.TrackBlockedFaultConfiguration()

    body = parser.parse(schema, request, location="json")

    return impl.component.update_track_blocked_fault_configuration(options, body)


@bp.route(
    "/component/fault-injection/track-blocked-fault/<identifier>", methods=["delete"]
)
def delete_track_blocked_fault_configuration(identifier):
    """Delete a track blocked fault configuration"""
    options = {}
    options["identifier"] = identifier

    return impl.component.delete_track_blocked_fault_configuration(options)


@bp.route("/component/fault-injection/track-speed-limit-fault", methods=["get"])
def get_track_speed_limit_fault_configuration_ids():
    """Get all track speed limit fault configuration ids"""
    options = {}
    options["simulationId"] = request.args.get("simulationId")

    return impl.component.get_track_speed_limit_fault_configuration_ids(options)


@bp.route("/component/fault-injection/track-speed-limit-fault", methods=["post"])
def create_track_speed_limit_fault_configuration():
    """Create a track speed limit fault configuration"""
    schema = model.TrackSpeedLimitFaultConfiguration()

    body = parser.parse(schema, request, location="json")

    return impl.component.create_track_speed_limit_fault_configuration(body)


@bp.route(
    "/component/fault-injection/track-split-limit-fault/<identifier>", methods=["get"]
)
def get_track_speed_limit_fault_configuration(identifier):
    """Get a track speed limit fault configuration"""
    options = {}
    options["identifier"] = identifier

    return impl.component.get_track_speed_limit_fault_configuration(options)


@bp.route(
    "/component/fault-injection/track-split-limit-fault/<identifier>", methods=["put"]
)
def update_track_speed_limit_fault_configuration(identifier):
    """Update a track speed limit fault configuration"""
    options = {}
    options["identifier"] = identifier

    schema = model.TrackSpeedLimitFaultConfiguration()

    body = parser.parse(schema, request, location="json")

    return impl.component.update_track_speed_limit_fault_configuration(options, body)


@bp.route(
    "/component/fault-injection/track-split-limit-fault/<identifier>",
    methods=["delete"],
)
def delete_track_speed_limit_fault_configuration(identifier):
    """Delete a track speed limit fault configuration"""
    options = {}
    options["identifier"] = identifier

    return impl.component.delete_track_speed_limit_fault_configuration(options)


@bp.route("/component/fault-injection/train-prio-fault", methods=["get"])
def get_train_prio_fault_configuration_ids():
    """Get all train prio fault configuration ids"""
    options = {}
    options["simulationId"] = request.args.get("simulationId")

    return impl.component.get_train_prio_fault_configuration_ids(options)


@bp.route("/component/fault-injection/train-prio-fault", methods=["post"])
def create_train_prio_fault_configuration():
    """Create a train prio fault configuration"""
    schema = model.TrainPrioFaultConfiguration()

    body = parser.parse(schema, request, location="json")

    return impl.component.create_train_prio_fault_configuration(body)


@bp.route("/component/fault-injection/train-prio-fault/<identifier>", methods=["get"])
def get_train_prio_fault_configuration(identifier):
    """Get a train prio fault configuration"""
    options = {}
    options["identifier"] = identifier

    return impl.component.get_train_prio_fault_configuration(options)


@bp.route("/component/fault-injection/train-prio-fault/<identifier>", methods=["put"])
def update_train_prio_fault_configuration(identifier):
    """Update a train prio fault configuration"""
    options = {}
    options["identifier"] = identifier

    schema = model.TrainPrioFaultConfiguration()

    body = parser.parse(schema, request, location="json")

    return impl.component.update_train_prio_fault_configuration(options, body)


@bp.route(
    "/component/fault-injection/train-prio-fault/<identifier>", methods=["delete"]
)
def delete_train_prio_fault_configuration(identifier):
    """Delete a train prio fault configuration"""
    options = {}
    options["identifier"] = identifier

    return impl.component.delete_train_prio_fault_configuration(options)


@bp.route("/component/fault-injection/train-speed-fault", methods=["get"])
def get_train_speed_fault_configuration_ids():
    """Get all train speed fault configuration ids"""
    options = {}
    options["simulationId"] = request.args.get("simulationId")

    return impl.component.get_train_speed_fault_configuration_ids(options)


@bp.route("/component/fault-injection/train-speed-fault", methods=["post"])
def create_train_speed_fault_configuration():
    """Create a train speed fault configuration"""
    schema = model.TrainSpeedFaultConfiguration()

    body = parser.parse(schema, request, location="json")

    return impl.component.create_train_speed_fault_configuration(body)


@bp.route("/component/fault-injection/train-speed-fault/<identifier>", methods=["get"])
def get_train_speed_fault_configuration(identifier):
    """Get a train speed fault configuration"""
    options = {}
    options["identifier"] = identifier

    return impl.component.get_train_speed_fault_configuration(options)


@bp.route("/component/fault-injection/train-speed-fault/<identifier>", methods=["put"])
def update_train_speed_fault_configuration(identifier):
    """Update a train speed fault configuration"""
    options = {}
    options["identifier"] = identifier

    schema = model.TrainSpeedFaultConfiguration()

    body = parser.parse(schema, request, location="json")

    return impl.component.update_train_speed_fault_configuration(options, body)


@bp.route(
    "/component/fault-injection/train-speed-fault/<identifier>", methods=["delete"]
)
def delete_train_speed_fault_configuration(identifier):
    """Delete a train speed fault configuration"""
    options = {}
    options["identifier"] = identifier

    return impl.component.delete_train_speed_fault_configuration(options)


@bp.route("/component/interlocking", methods=["get"])
def get_interlocking_configuration_ids():
    """Get all interlocking configuration ids"""
    options = {}
    options["simulationId"] = request.args.get("simulationId")

    return impl.component.get_interlocking_configuration_ids(options)


@bp.route("/component/interlocking", methods=["post"])
def create_interlocking_configuration():
    """Create a interlocking configuration"""
    schema = model.InterlockingConfiguration()

    body = parser.parse(schema, request, location="json")

    return impl.component.create_interlocking_configuration(body)


@bp.route("/component/interlocking/<identifier>", methods=["get"])
def get_interlocking_configuration(identifier):
    """Get a interlocking configuration"""
    options = {}
    options["identifier"] = identifier

    return impl.component.get_interlocking_configuration(options)


@bp.route("/component/interlocking/<identifier>", methods=["put"])
def update_interlocking_configuration(identifier):
    """Update a interlocking configuration"""
    options = {}
    options["identifier"] = identifier

    schema = model.InterlockingConfiguration()

    body = parser.parse(schema, request, location="json")

    return impl.component.update_interlocking_configuration(options, body)


@bp.route("/component/interlocking/<identifier>", methods=["delete"])
def delete_interlocking_configuration(identifier):
    """Delete a interlocking configuration"""
    options = {}
    options["identifier"] = identifier

    return impl.component.delete_interlocking_configuration(options)


@bp.route("/component/spawner", methods=["get"])
def get_spawner_configuration_ids():
    """Get all spawner configuration ids"""
    options = {}
    options["simulationId"] = request.args.get("simulationId")

    return impl.component.get_spawner_configuration_ids(options)


@bp.route("/component/spawner", methods=["post"])
def create_spawner_configuration():
    """Create a spawner configuration"""
    schema = model.SpawnerConfiguration()

    body = parser.parse(schema, request, location="json")

    return impl.component.create_spawner_configuration(body)


@bp.route("/component/spawner/<identifier>", methods=["get"])
def get_spawner_configuration(identifier):
    """Get a spawner configuration"""
    options = {}
    options["identifier"] = identifier

    return impl.component.get_spawner_configuration(options)


@bp.route("/component/spawner/<identifier>", methods=["put"])
def update_spawner_configuration(identifier):
    """Update a spawner configuration"""
    options = {}
    options["identifier"] = identifier

    schema = model.SpawnerConfiguration()

    body = parser.parse(schema, request, location="json")

    return impl.component.update_spawner_configuration(options, body)


@bp.route("/component/spawner/<identifier>", methods=["delete"])
def delete_spawner_configuration(identifier):
    """Delete a spawner configuration"""
    options = {}
    options["identifier"] = identifier

    return impl.component.delete_spawner_configuration(options)
