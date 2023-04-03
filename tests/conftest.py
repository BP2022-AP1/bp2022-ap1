from dotenv import load_dotenv


# pylint: disable-next=unused-argument
def pytest_configure(config):
    """
    Load environment variables before tests are run.
    """
    load_dotenv(".env.test")
