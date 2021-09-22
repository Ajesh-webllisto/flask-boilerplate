import logging.config
from os import environ

from celery import Celery
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from .config import config as app_config

celery = Celery(__name__)
db = SQLAlchemy()


def create_app():
    # loading env vars from .env file
    load_dotenv()
    APPLICATION_ENV = get_environment()
    logging.config.dictConfig(app_config[APPLICATION_ENV].LOGGING)
    app = Flask(app_config[APPLICATION_ENV].APP_NAME)
    app.config.from_object(app_config[APPLICATION_ENV])
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///boilerplate.db'

    CORS(app, resources={r'/api/*': {'origins': '*'}})
    db.init_app(app)
    celery.config_from_object(app.config, force=True)
    # celery is not able to pick result_backend and hence using update
    celery.conf.update(result_backend=app.config['RESULT_BACKEND'])

    from .core.views import core as core_blueprint
    from .accounts.views import accounts as accounts_blueprint
    from .accounts import models

    with app.app_context():
        db.create_all()
    app.register_blueprint(
        core_blueprint,
        url_prefix='/api/v1/core'
    )

    app.register_blueprint(
        accounts_blueprint,
        url_prefix='/accounts'
    )

    return app


def get_environment():
    return environ.get('APPLICATION_ENV') or 'development'
