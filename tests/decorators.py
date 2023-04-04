from functools import wraps
from typing import Callable

from src.base_model import db
from src.constants import tables


def recreate_db(func: Callable):
    """Decorates a test function and will recreate the database
    before calling the function.

    :param func: The test function to decorate
    :return: The decorated test function
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        db.drop_tables(tables)
        db.create_tables(tables)
        return func(*args, **kwargs)

    return wrapper


def recreate_db_setup(func: Callable):
    """Decorates a test setup function and will recreate the database
    before calling the function.

    :param func: The test setup function to decorate
    :return: The decorated test setup function
    """

    @wraps(func)
    def wrapper(method: Callable, *args, **kwargs):
        db.drop_tables(tables)
        db.create_tables(tables)
        return func(method, *args, **kwargs)

    return wrapper
