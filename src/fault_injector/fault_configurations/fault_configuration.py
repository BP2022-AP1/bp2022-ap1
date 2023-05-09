from peewee import FloatField, IntegerField, TextField

from src.base_model import SerializableBaseModel


class FaultConfiguration(SerializableBaseModel):
    """Class that contains the attributes of the Fault class"""

    start_tick = IntegerField(null=True)
    end_tick = IntegerField(null=True)
    inject_probability = FloatField(null=True)
    resolve_probability = FloatField(null=True)
    strategy = TextField()

    # - affected_element_ID: int = None // has to be implemented in subclasses
    description = TextField(default="injected Fault")

    def to_dict(self):
        data = super().to_dict()
        return {
            "start_tick": self.start_tick,
            "end_tick": self.end_tick,
            "inject_probability": self.inject_probability,
            "resolve_probability": self.resolve_probability,
            "description": self.description,
            "strategy": self.strategy,
            **data,
        }
