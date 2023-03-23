from dotenv import dotenv_values
import os

constants = {
    **dotenv_values(".env.test"),  # load shared development variables
    **os.environ,  # override loaded values with environment variables
}