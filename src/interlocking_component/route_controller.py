import marshmallow as marsh
from peewee import BooleanField

from src.base_model import BaseModel
from src.component import Component


class InterlockingConfiguration(BaseModel):
    """Ths class contains all fiels needed to configure the Interlocking and the RouteController
    """
    class Schema(BaseModel.Schema):
        dynamicRouting = marsh.fields.Boolean()

        def _make(self, data: dict) -> "InterlockingConfiguration":
            return InterlockingConfiguration(**data)

    dynamicRouting = BooleanField(default=True)


class RouteController(Component):
    """This class coordinates the route of a train.
    It calls the router to find a route for a train.
    It makes sure, that the Interlocking sets fahrstrassen along those routes.
    """

    def next_tick(self, tick: int):
        """This may be called to process a new simulation tick.

        :param tick: The current tick of the simulation.
        :type tick: int
        :raises NotImplementedError: This has not yet been implemented.
        """
        raise NotImplementedError()
