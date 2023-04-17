from src.interlocking_component.route_controller import InterlockingConfiguration


def test_default_true():
    """This test if an InterlockingConfiguration Object can be initialized
    and if the default for dynamicRouting is false."""
    interlocking_configuration = InterlockingConfiguration()
    assert not interlocking_configuration.dynamicRouting
