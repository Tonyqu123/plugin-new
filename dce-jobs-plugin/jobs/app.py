#!/usr/bin/env python

import os
import sys
import logging
from flask import Flask
from flask import request
from flask_cors import CORS
from executor import Executor
from executor import DB_NAME
from api import load_api
from docker_client import init_global_agent_service
from storage import init_config

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))


def setup_app(app):
    @app.before_request
    def get_info_from_header():
        request.token = request.headers.get('X-DCE-Access-Token') or request.cookies.get('DCE_TOKEN')
        request.tenant = request.headers.get('DCE-TENANT') or request.cookies.get('DCE_TENANT')


LOG_LEVEL = logging.INFO # if PROD else logging.DEBUG


def init_logging(level=None):
    level = level or LOG_LEVEL
    console_handler = logging.StreamHandler(sys.stderr)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    console_handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.addHandler(console_handler)
    root_logger.setLevel(level)

    # setup logging level
    logging.getLogger('requests').propagate = False
    logging.getLogger('docker').level = logging.ERROR


def init_db():
    if not os.path.exists(DB_NAME):
        Executor.init_db()


def __init():
    init_logging()
    init_config()
    init_global_agent_service()
    init_db()


__init()


def create_app(name=None):
    app = Flask(name or __name__)
    CORS(app)
    app.debug = False
    setup_app(app)
    load_api(app)

    return app


app = create_app()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
