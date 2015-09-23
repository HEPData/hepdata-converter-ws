# -*- encoding: utf-8 -*-

from flask.app import Flask
import hepdata_converter_ws

__author__ = 'Michał Szostak'

# configuration
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'


def create_app(config_filename=None):
    app = Flask(__name__)
    app.config.from_object(hepdata_converter_ws)

    from hepdata_converter_ws.api import api
    app.register_blueprint(api)

    return app


def main():
    app = create_app()
    app.run()