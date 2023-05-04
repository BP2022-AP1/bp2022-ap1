import abc
import os

from celery import Celery, Task
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

    app.config.from_mapping(
        CELERY={
            "broker_url": os.environ["CELERY_BROKER_URL"],
            "result_backend": os.environ["CELERY_RESULT_BACKEND"],
            "task_ignore_result": True,
        }
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    app.config.from_prefixed_env()
    celery_init_app(app)

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


def celery_init_app(app: Flask) -> Celery:
    """Initialize celery instance and wrap around flask app"""

    class FlaskTask(Task):
        """Wrap celery task around flask app"""

        @abc.abstractmethod
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app
