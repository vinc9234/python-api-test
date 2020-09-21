# coding: utf-8

from tests import BaseTestCase


class TestPublicController(BaseTestCase):
    """PublicController integration test stubs"""

    def setUp(self) -> None:
        for i in range(10):
            data = {"a": i, "b": "ciao"}
            response = self.client.open("/store/v1/items", method="POST", json=data)

    def test_post_items(self):
        """Test case for post_item

        Inserisce un oggetto nello store.
        """
        data = {"a": 1, "b": "ciao"}
        response = self.client.open("/store/v1/items", method="POST", json=data)
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))
        assert "id" in response.json

    def test_get_items(self):
        """Test case for get_items

        Recupera un elenco di oggetti dallo store.
        """
        response = self.client.open("/store/v1/items", method="GET")
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))
        assert response.json["limit"] == 10
        assert response.json["count"] == 10
        assert len(response.json["items"]) == response.json["count"]

    def test_get_items_limit(self):
        """Test case for get_items

        Recupera un elenco di oggetti dallo store.
        """
        limit = 7
        response = self.client.open(f"/store/v1/items?limit={limit}", method="GET")
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))
        assert response.json["limit"] == limit
        assert response.json["count"] == limit
        assert len(response.json["items"]) == limit

    def test_get_items_limit_above(self):
        """Test case for get_items

        Recupera un elenco di oggetti dallo store.
        """
        limit = 101
        response = self.client.open(f"/store/v1/items?limit={limit}", method="GET")
        self.assert400(response, "Response body is : " + response.data.decode("utf-8"))

    def test_get_item(self):
        """Test case for get_echo

        Recupera un oggetto dallo store.
        """
        response = self.client.open("/store/v1/items", method="GET")
        uuid = response.json["items"][0]["id"]
        response = self.client.open(f"/store/v1/item/{uuid}", method="GET")
        self.assert200(response, "Response body is : " + response.data.decode("utf-8"))

    def test_get_status(self):
        """Test case for get_status

        Ritorna lo stato dell'applicazione.
        """
        response = self.client.open("/store/v1/status", method="GET")
        if response.status_code == 200:
            self.assert200(
                response, "Response body is : " + response.data.decode("utf-8")
            )
        elif response.status_code == 503:
            self.assertTrue("random" in response.data.decode("utf-8"))

        assert "no-store" == response.headers.get("cache-control")
