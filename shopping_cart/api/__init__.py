import sys

import yaml
from flask import Flask
from flask_cors import CORS

from api.datamodel import DataModels  # noqa F401
from api.datamodel import db
from api.log_utils import logger


def create_app(config=None):
    if config is None:
        print("Please provide a config file.")
        sys.exit(1)
    with open(config, "r") as conf_file:
        cfg = yaml.load(conf_file)

    app = Flask(__name__)
    app.config.update(cfg)
    app.secret_key = "mysecretkey"

    # setup specifics for sqlalchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        "postgresql://{0}:{1}@{2}/{3}".format(cfg['pg']['user'],
                                              cfg['pg']['pw'],
                                              cfg['pg']['host'],
                                              cfg['pg']['db'])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_NATIVE_UNICODE'] = True
    db.init_app(app)

    # deal with CORS
    CORS(app)
    logger(app)

    # register the endpoints
    register_blueprints(app)

    return app


def register_blueprints(app):
    """Register blueprints on prepared app in create_app()"""
    from api.endpoints import (index_bp, hello_world_bp,
                               master_data_insert_bp,
                               master_data_delete_bp,
                               master_data_update_bp,
                               master_data_get_for_column_bp,
                               master_data_get_for_table_bp)

    app.register_blueprint(index_bp)
    app.register_blueprint(hello_world_bp)
    app.register_blueprint(master_data_insert_bp)
    app.register_blueprint(master_data_delete_bp)
    app.register_blueprint(master_data_update_bp)
    app.register_blueprint(master_data_get_for_column_bp)
    app.register_blueprint(master_data_get_for_table_bp)
