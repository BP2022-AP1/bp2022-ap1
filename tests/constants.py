import os
from dotenv import dotenv_values

constants = {
    **dotenv_values(".env.test"),  # load shared development variables
    **os.environ,  # override loaded values with environment variables
}
