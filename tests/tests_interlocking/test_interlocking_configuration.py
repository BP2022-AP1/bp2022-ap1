from src.interlocking_component.route_controller import InterlockingConfiguration


def test_initialisation():
    interlockingConfiguration = InterlockingConfiguration
    assert interlockingConfiguration.dynamicRouting
