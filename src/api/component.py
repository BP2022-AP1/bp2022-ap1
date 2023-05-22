from flask import Blueprint, request
from webargs.flaskparser import parser

from src import implementor as impl
from src.api import schemas
from src.api.decorators import token_required

bp = Blueprint("component", __name__)


@bp.route("/component/fault-injection/schedule-blocked-fault", methods=["get"])
@token_required()
def get_all_schedule_blocked_fault_configuration_ids(token):
    """Get all schedule blocked fault configuration ids"""
    options = {}
    options["simulationId"] = request.args.get("simulationId")

    return impl.component.get_all_schedule_blocked_fault_configuration_ids(
        options, token
    )


@bp.route("/component/fault-injection/schedule-blocked-fault", methods=["post"])
@token_required()
def create_schedule_blocked_fault_configuration(token):
    """Create a schedule blocked fault configuration"""
    schema = schemas.ScheduleBlockedFaultConfiguration()

    body = parser.parse(schema, request, location="json")

    return impl.component.create_schedule_blocked_fault_configuration(body, token)


@bp.route(
    "/component/fault-injection/schedule-blocked-fault/<identifier>", methods=["get"]
)
@token_required()
def get_schedule_blocked_fault_configuration(identifier, token):
    """Get a schedule blocked fault configuration"""
    options = {}
    options["identifier"] = identifier

    return impl.component.get_schedule_blocked_fault_configuration(options, token)


@bp.route(
    "/component/fault-injection/schedule-blocked-fault/<identifier>", methods=["delete"]
)
@token_required()
def delete_schedule_blocked_fault_configuration(identifier, token):
    """Delete a schedule blocked fault configuration"""
    options = {}
    options["identifier"] = identifier

    return impl.component.delete_schedule_blocked_fault_configuration(options, token)


@bp.route("/component/fault-injection/track-blocked-fault", methods=["get"])
@token_required()
def get_all_track_blocked_fault_configuration_ids(token):
    """Get all track blocked fault configuration ids"""
    options = {}
    options["simulationId"] = request.args.get("simulationId")

    return impl.component.get_all_track_blocked_fault_configuration_ids(options, token)


@bp.route("/component/fault-injection/track-blocked-fault", methods=["post"])
@token_required()
def create_track_blocked_fault_configuration(token):
    """Create a track blocked fault configuration"""
    schema = schemas.TrackBlockedFaultConfiguration()

    body = parser.parse(schema, request, location="json")

    return impl.component.create_track_blocked_fault_configuration(body, token)


@bp.route(
    "/component/fault-injection/track-blocked-fault/<identifier>", methods=["get"]
)
@token_required()
def get_track_blocked_fault_configuration(identifier, token):
    """Get a track blocked fault configuration"""
    options = {}
    options["identifier"] = identifier

    return impl.component.get_track_blocked_fault_configuration(options, token)


@bp.route(
    "/component/fault-injection/track-blocked-fault/<identifier>", methods=["delete"]
)
@token_required()
def delete_track_blocked_fault_configuration(identifier, token):
    """Delete a track blocked fault configuration"""
    options = {}
    options["identifier"] = identifier

    return impl.component.delete_track_blocked_fault_configuration(options, token)


@bp.route("/component/fault-injection/track-speed-limit-fault", methods=["get"])
@token_required()
def get_all_track_speed_limit_fault_configuration_ids(token):
    """Get all track speed limit fault configuration ids"""
    options = {}
    options["simulationId"] = request.args.get("simulationId")

    return impl.component.get_all_track_speed_limit_fault_configuration_ids(
        options, token
    )


@bp.route("/component/fault-injection/track-speed-limit-fault", methods=["post"])
@token_required()
def create_track_speed_limit_fault_configuration(token):
    """Create a track speed limit fault configuration"""
    schema = schemas.TrackSpeedLimitFaultConfiguration()

    body = parser.parse(schema, request, location="json")

    return impl.component.create_track_speed_limit_fault_configuration(body, token)


@bp.route(
    "/component/fault-injection/track-speed-limit-fault/<identifier>", methods=["get"]
)
@token_required()
def get_track_speed_limit_fault_configuration(identifier, token):
    """Get a track speed limit fault configuration"""
    options = {}
    options["identifier"] = identifier

    return impl.component.get_track_speed_limit_fault_configuration(options, token)


@bp.route(
    "/component/fault-injection/track-speed-limit-fault/<identifier>",
    methods=["delete"],
)
@token_required()
def delete_track_speed_limit_fault_configuration(identifier, token):
    """Delete a track speed limit fault configuration"""
    options = {}
    options["identifier"] = identifier

    return impl.component.delete_track_speed_limit_fault_configuration(options, token)


@bp.route("/component/fault-injection/train-prio-fault", methods=["get"])
@token_required()
def get_all_train_prio_fault_configuration_ids(token):
    """Get all train prio fault configuration ids"""
    options = {}
    options["simulationId"] = request.args.get("simulationId")

    return impl.component.get_all_train_prio_fault_configuration_ids(options, token)


@bp.route("/component/fault-injection/train-prio-fault", methods=["post"])
@token_required()
def create_train_prio_fault_configuration(token):
    """Create a train prio fault configuration"""
    schema = schemas.TrainPrioFaultConfiguration()

    body = parser.parse(schema, request, location="json")

    return impl.component.create_train_prio_fault_configuration(body, token)


@bp.route("/component/fault-injection/train-prio-fault/<identifier>", methods=["get"])
@token_required()
def get_train_prio_fault_configuration(identifier, token):
    """Get a train prio fault configuration"""
    options = {}
    options["identifier"] = identifier

    return impl.component.get_train_prio_fault_configuration(options, token)


@bp.route(
    "/component/fault-injection/train-prio-fault/<identifier>", methods=["delete"]
)
@token_required()
def delete_train_prio_fault_configuration(identifier, token):
    """Delete a train prio fault configuration"""
    options = {}
    options["identifier"] = identifier

    return impl.component.delete_train_prio_fault_configuration(options, token)


@bp.route("/component/fault-injection/train-speed-fault", methods=["get"])
@token_required()
def get_all_train_speed_fault_configuration_ids(token):
    """Get all train speed fault configuration ids"""
    options = {}
    options["simulationId"] = request.args.get("simulationId")

    return impl.component.get_all_train_speed_fault_configuration_ids(options, token)


@bp.route("/component/fault-injection/train-speed-fault", methods=["post"])
@token_required()
def create_train_speed_fault_configuration(token):
    """Create a train speed fault configuration"""
    schema = schemas.TrainSpeedFaultConfiguration()

    body = parser.parse(schema, request, location="json")

    return impl.component.create_train_speed_fault_configuration(body, token)


@bp.route("/component/fault-injection/train-speed-fault/<identifier>", methods=["get"])
@token_required()
def get_train_speed_fault_configuration(identifier, token):
    """Get a train speed fault configuration"""
    options = {}
    options["identifier"] = identifier

    return impl.component.get_train_speed_fault_configuration(options, token)


@bp.route(
    "/component/fault-injection/train-speed-fault/<identifier>", methods=["delete"]
)
@token_required()
def delete_train_speed_fault_configuration(identifier, token):
    """Delete a train speed fault configuration"""
    options = {}
    options["identifier"] = identifier

    return impl.component.delete_train_speed_fault_configuration(options, token)


@bp.route("/component/fault-injection/platform-blocked-fault", methods=["get"])
@token_required()
def get_all_platform_blocked_fault_configuration_ids(token):
    """Get all platform blocked fault configuration ids"""
    options = {}
    options["simulationId"] = request.args.get("simulationId")

    return impl.component.get_all_platform_blocked_fault_configuration_ids(
        options, token
    )


@bp.route("/component/fault-injection/platform-blocked-fault", methods=["post"])
@token_required()
def create_platform_blocked_fault_configuration(token):
    """Create a platform blocked fault configuration"""
    schema = schemas.PlatformBlockedFaultConfiguration()

    body = parser.parse(schema, request, location="json")

    return impl.component.create_platform_blocked_fault_configuration(body, token)


@bp.route(
    "/component/fault-injection/platform-blocked-fault/<identifier>", methods=["get"]
)
@token_required()
def get_platform_blocked_fault_configuration(identifier, token):
    """Get a platform blocked fault configuration"""
    options = {}
    options["identifier"] = identifier

    return impl.component.get_platform_blocked_fault_configuration(options, token)


@bp.route(
    "/component/fault-injection/platform-blocked-fault/<identifier>", methods=["delete"]
)
@token_required()
def delete_platform_blocked_fault_configuration(identifier, token):
    """Delete a platform blocked fault configuration"""
    options = {}
    options["identifier"] = identifier

    return impl.component.delete_platform_blocked_fault_configuration(options, token)


@bp.route("/component/interlocking", methods=["get"])
@token_required()
def get_all_interlocking_configuration_ids(token):
    """Get all interlocking configuration ids"""
    options = {}
    options["simulationId"] = request.args.get("simulationId")

    return impl.component.get_all_interlocking_configuration_ids(options, token)


@bp.route("/component/interlocking", methods=["post"])
@token_required()
def create_interlocking_configuration(token):
    """Create a interlocking configuration"""
    schema = schemas.InterlockingConfiguration()

    body = parser.parse(schema, request, location="json")

    return impl.component.create_interlocking_configuration(body, token)


@bp.route("/component/interlocking/<identifier>", methods=["get"])
@token_required()
def get_interlocking_configuration(identifier, token):
    """Get a interlocking configuration"""
    options = {}
    options["identifier"] = identifier

    return impl.component.get_interlocking_configuration(options, token)


@bp.route("/component/interlocking/<identifier>", methods=["delete"])
@token_required()
def delete_interlocking_configuration(identifier, token):
    """Delete a interlocking configuration"""
    options = {}
    options["identifier"] = identifier

    return impl.component.delete_interlocking_configuration(options, token)


@bp.route("/component/spawner", methods=["get"])
@token_required()
def get_all_spawner_configuration_ids(token):
    """Get all spawner configuration ids"""
    options = {}
    options["simulationId"] = request.args.get("simulationId")

    return impl.component.get_all_spawner_configuration_ids(options, token)


@bp.route("/component/spawner", methods=["post"])
@token_required()
def create_spawner_configuration(token):
    """Create a spawner configuration"""
    schema = schemas.SpawnerConfiguration()

    body = parser.parse(schema, request, location="json")

    return impl.component.create_spawner_configuration(body, token)


@bp.route("/component/spawner/<identifier>", methods=["get"])
@token_required()
def get_spawner_configuration(identifier, token):
    """Get a spawner configuration"""
    options = {}
    options["identifier"] = identifier

    return impl.component.get_spawner_configuration(options, token)


@bp.route("/component/spawner/<identifier>", methods=["delete"])
@token_required()
def delete_spawner_configuration(identifier, token):
    """Delete a spawner configuration"""
    options = {}
    options["identifier"] = identifier

    return impl.component.delete_spawner_configuration(options, token)
