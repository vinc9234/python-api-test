#!/usr/bin/env python3

from logging import basicConfig
from logging.config import dictConfig
from os import environ as env
from os.path import isfile

import connexion
import pymongo
import yaml
from connexion import problem

from api.errors import handle_write_error
from api.store import MongoStore, Store


def configure_logger(log_config="logging.yaml"):
    """Configure the logging subsystem."""
    if not isfile(log_config):
        return basicConfig()

    with open(log_config) as fh:
        log_config = yaml.safe_load(fh)
        return dictConfig(log_config)


def main():
    configure_logger()

    app = connexion.App(__name__, specification_dir="../openapi/")
    app.add_api("store.yaml", arguments={"title": "Store items."})

    app.add_error_handler(pymongo.errors.WriteError, handle_write_error)

    @app.app.before_first_request
    def create_store():
        if env.get("MONGO_HOST"):
            app.app.config["store"] = MongoStore(
                host=env["MONGO_HOST"],
                username=env["MONGO_USER"],
                password=env["MONGO_PASSWORD"],
            )
            return
        app.app.config["store"] = Store()

    app.run(port=8443, ssl_context="adhoc", debug=True)


if __name__ == "__main__":
    main()
