import schemathesis
from tests import BaseTestCase


app = BaseTestCase().create_app()

schema = schemathesis.from_wsgi("/store/v1/openapi.yaml", app)

schemathesis_config = dict(endpoint="/store/v1/items", method="POST")


@schema.parametrize(**schemathesis_config)
def test_no_server_errors(case):
    response = case.call_wsgi()
    assert response.status_code < 500
