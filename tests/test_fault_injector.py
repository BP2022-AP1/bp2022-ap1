import json

from src.fault_injector.fault_types.train_fault import TrainFault


def test_json_schema_1():
    test_fault = TrainFault()
    assert test_fault.check_json(
        json.loads(
            """{
                    "faultID" : 1, 
                    "startTick" : 2, 
                    "endTick" : 3, 
                    "affectedElementID" : 4, 
                    "description" : "2"
                }"""
        )
    )


def test_json_schema_2():
    test_fault = TrainFault()
    assert not (
        test_fault.check_json(
            json.loads(
                """{
                    "faultID" : 2, 
                    "startTick" : 2, 
                    "endTick" : 3,
                    "affectedElementID" : 4, 
                    "description" : "2"
                }"""
            )
        )
    )
