import os

from flask import Flask

from .api import component, run, schedule, simulation, token


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY="dev")
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
    app.register_blueprint(component.bp)
    app.register_blueprint(run.bp)
    app.register_blueprint(schedule.bp)
    app.register_blueprint(simulation.bp)
    app.register_blueprint(token.bp)

    return app
