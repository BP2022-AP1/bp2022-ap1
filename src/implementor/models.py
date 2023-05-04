from peewee import CharField, ForeignKeyField

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
        return {"description": self.description, **data}


class Run(SerializableBaseModel):
    """Represents the configuration of a single execution of a simulation configuration."""

    simulation_configuration = ForeignKeyField(SimulationConfiguration, backref="runs")

    def to_dict(self):
        data = super().to_dict()
        return {
            "simulation": str(self.simulation_configuration.id),
            **data,
        }
