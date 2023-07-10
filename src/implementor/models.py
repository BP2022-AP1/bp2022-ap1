from peewee import CharField, ForeignKeyField, UUIDField

from src.base_model import SerializableBaseModel


class Token(SerializableBaseModel):
    """Represents a token."""

    permission = CharField()
    name = CharField()
    hashedToken = CharField()

    def to_dict(self):
        data = super().to_dict()
        return {"permission": self.permission, "name": self.name, **data}


class SimulationConfiguration(SerializableBaseModel):
    """Represents a single simulation configuration."""

    description = CharField(null=True)

    def to_dict(self):
        data = super().to_dict()
        spawner_ids = [
            str(reference.spawner_configuration.id)
            # It is a peewee method
            # pylint: disable-next=no-member
            for reference in self.spawner_configuration_references
        ]
        # Should be only one spawner
        spawner_id = spawner_ids[0] if len(spawner_ids) > 0 else None

        platform_blocked_fault_ids = [
            str(reference.platform_blocked_fault_configuration.id)
            # It is a peewee method
            # pylint: disable-next=no-member
            for reference in self.platform_blocked_fault_configuration_references
        ]

        schedule_blocked_fault_ids = [
            str(reference.schedule_blocked_fault_configuration.id)
            # It is a peewee method
            # pylint: disable-next=no-member
            for reference in self.schedule_blocked_fault_configuration_references
        ]

        track_blocked_fault_ids = [
            str(reference.track_blocked_fault_configuration.id)
            # It is a peewee method
            # pylint: disable-next=no-member
            for reference in self.track_blocked_fault_configuration_references
        ]

        track_speed_limit_fault_ids = [
            str(reference.track_speed_limit_fault_configuration.id)
            # It is a peewee method
            # pylint: disable-next=no-member
            for reference in self.track_speed_limit_fault_configuration_references
        ]

        train_speed_fault_ids = [
            str(reference.train_speed_fault_configuration.id)
            # It is a peewee method
            # pylint: disable-next=no-member
            for reference in self.train_speed_fault_configuration_references
        ]

        train_prio_fault_ids = [
            str(reference.train_prio_fault_configuration.id)
            #  It is a peewee method
            # pylint: disable-next=no-member
            for reference in self.train_prio_fault_configuration_references
        ]
        # pylint: disable-next=no-member
        run_ids = [str(run.id) for run in self.runs]
        return {
            "description": self.description,
            "spawner": spawner_id,
            "platform_blocked_fault": platform_blocked_fault_ids,
            "schedule_blocked_fault": schedule_blocked_fault_ids,
            "track_blocked_fault": track_blocked_fault_ids,
            "track_speed_limit_fault": track_speed_limit_fault_ids,
            "train_speed_fault": train_speed_fault_ids,
            "train_prio_fault": train_prio_fault_ids,
            "runs": run_ids,
            **data,
        }


class Run(SerializableBaseModel):
    """Represents the configuration of a single execution of a simulation configuration."""

    simulation_configuration = ForeignKeyField(SimulationConfiguration, backref="runs")
    process_id = UUIDField(null=True)

    def to_dict(self):
        data = super().to_dict()
        return {
            "simulation": str(self.simulation_configuration.id),
            "process_id": str(self.process_id),
            **data,
        }
