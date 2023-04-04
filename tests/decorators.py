from functools import wraps
from typing import Callable

from src.base_model import db
from src.constants import tables


def recreate_db(func: Callable):
    """Decorates a function and will recreate the database
    before calling the function.

    :param func: The function to decorate
    :return: The decorated function
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        db.drop_tables(tables)
        db.create_tables(tables)
        return func(*args, **kwargs)

    return wrapper
