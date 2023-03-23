from src.fault_injector.fault_types.train_fault import TrainFault
import json


def test_json_schema():
    test_fault = TrainFault()
    assert (
        test_fault.check_json(
            json.loads(
                '{"faultID" : 1, "startTick" : 2, "endTick" : 3, "affectedElementID" : 4, "description" : "2"}'
            )
        )
        == False
    )


def test_json_schema():
    test_fault = TrainFault()
    assert (
        test_fault.check_json(
            json.loads(
                '{"faultID" : 2, "startTick" : 2, "endTick" : 3, "affectedElementID" : 4, "description" : "2"}'
            )
        )
        == True
    )
