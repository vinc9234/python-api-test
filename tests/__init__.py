import logging

import connexion
from flask_testing import TestCase

from api.store import MongoStore, Store
import pymongo
from api.errors import handle_write_error


class BaseTestCase(TestCase):
    def create_app(self):
        """
        This method sets up the class automatically.
        """
        logging.getLogger("connexion.operation").setLevel("ERROR")
        app = connexion.App(__name__, specification_dir="../openapi/")
        app.add_api("store.yaml")
        app.add_error_handler(pymongo.errors.WriteError, handle_write_error)

        @app.app.before_first_request
        def create_store():
            """
            Which DBMS are we using to run our tests?
            Can you fix that?
            :return:
            """
            config = dict(host="mongo", username="root", password="secret")  # nosec
            app.app.config["store"] = MongoStore(**config)

        return app.app
