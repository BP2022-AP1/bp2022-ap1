"""
A basic test sample
"""

def inc(num : int):
    """
    A basic increment function

    :rtype: int
    """
    return num + 1


def test_answer():
    """
    A basic test

    :return: None
    """
    assert inc(4) == 5
