import json
import os
from abc import ABC, abstractmethod

import jsonschema

from src.component import Component


class Fault(ABC):
    """An abstract fault for the fault injection"""

    start_tick: int = None
    end_tick: int = None
    component: Component = None
    affected_element_ID: int = None
    description: str = "injected fault"
    _fault_types: dict = {}

    @classmethod
    @abstractmethod
    def from_json(cls, json_object: str) -> "Fault":
        """constructs an fault object from a JSON object

        :param json_object: a json object containing the relevant info for the fault
        :type json_object: string
        :return: a fault
        :rtype: Fault
        """

        raise NotImplementedError()

    def check_json(self, json_object: str) -> bool:
        """checks if a given json object conforms the json schema for faults

        :param json_object: the json object being validated
        :type json_object: str
        :return: returns if the given json object is valid according to the json schema
        :rtype: bool
        """
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, "./../fault_json_schema.json")
        json_schema = json.load(open(filename, "r"))
        # jsonschema.validate(instance=json_object, schema=json_schema)
        print(json_object)
        return jsonschema.Draft202012Validator(json_schema).is_valid(json_object)

    @abstractmethod
    def inject_fault(component: Component):
        """injects the fault into the given component

        :param component: the component the fault should be injected into
        :type component: Component
        """

        raise NotImplementedError()
