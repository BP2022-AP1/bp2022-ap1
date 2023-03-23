import os

from dotenv import dotenv_values

constants: dict[str, str | None] = {
    **dotenv_values(".env.test"),  # load shared development variables
    **os.environ,  # override loaded values with environment variables
}
