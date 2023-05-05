import abc
import os

from flask import Flask

from src.api.component import bp as component_bp
from src.api.run import bp as run_bp
from src.api.schedule import bp as schedule_bp
from src.api.simulation import bp as simulation_bp
from src.api.token import bp as token_bp


def create_app(test_config=None) -> Flask:
    """
    Create a flask app.
    Add test configuration of you want to run the app in test mode.

    :param test_config: A dictionary containing the test configuration
    :return: A flask app
    """
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        print(f"Instance path = {app.instance_path}")
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Add blueprints
    app.register_blueprint(component_bp)
    app.register_blueprint(run_bp)
    app.register_blueprint(schedule_bp)
    app.register_blueprint(simulation_bp)
    app.register_blueprint(token_bp)

    return app
