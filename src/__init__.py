import abc
import json
import os
from os.path import join

from flask import Flask
from grafana_pandas_datasource.service import pandas_component
from requests import RequestException, post

import src.data_science
from src.api.component import bp as component_bp
from src.api.run import bp as run_bp
from src.api.schedule import bp as schedule_bp
from src.api.simulation import bp as simulation_bp
from src.api.token import bp as token_bp
from src.data_science.grafana_data_registration import define_and_register_data
from src.implementor.models import Token
from src.implementor.permission import Permission
from src.implementor.token import hash_token


def _post_data(path, data):
    try:
        return post(
            path,
            json=data,
            auth=("admin", os.environ["GF_SECURITY_ADMIN_PASSWORD"]),
            timeout=10,
        )
    except RequestException as exception:
        print("An exception while initializing Grafana occurred\n", exception)
        return None


def initialize_grafana():
    """Initialize Grafana"""
    with open("grafana/local/datasource.json", "r", encoding="UTF-8") as file:
        data_source = json.load(file)
    result = _post_data(
        f"http://{os.environ['GRAFANA_HOST']}:3000/api/datasources", data_source
    )
    if result is None:
        return
    try:
        data_source_uid = result.json()["datasource"]["uid"]
    except KeyError as exception:
        print("An exception while initializing Grafana occurred\n", exception)
        return

    dashboard_list = [
        "dashboard_run_based.json",
        "dashboard_config_based.json",
        "dashboard_multi_config_based.json",
    ]
    for dashboard_name in dashboard_list:
        with open(join("grafana/local", dashboard_name), "r", encoding="UTF-8") as file:
            file_json = json.load(file)
            file_str = json.dumps(file_json).replace("DATASOURCE_UID", data_source_uid)
            data_dashboard = json.loads(file_str)
            data_dashboard = {
                "dashboard": data_dashboard,
            }
            _post_data(
                f"http://{os.environ['GRAFANA_HOST']}:3000/api/dashboards/db",
                data_dashboard,
            )


def insert_first_token():
    """
    Insert first admin token defined in env variables.
    """
    name = "first-admin-token"
    permission = Permission.ADMIN.value
    clear_token = os.getenv("FIRST_ADMIN_TOKEN", None)
    if clear_token is not None:
        hashed_token = hash_token(clear_token)
        if (
            Token.select()
            .where(
                (Token.hashedToken == hashed_token)
                & (Token.name == name)
                & (Token.permission == permission)
            )
            .exists()
        ):
            return
        Token.create(hashedToken=hashed_token, permission=permission, name=name)


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
    app.register_blueprint(pandas_component, url_prefix="/pandas-component")

    define_and_register_data()
    initialize_grafana()
    insert_first_token()

    return app
