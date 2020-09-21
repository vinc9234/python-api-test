import logging

import pytest

from api.store import MongoStore, Store

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


@pytest.fixture(
    scope="module",
    params=[
        (Store, {}),
        (MongoStore, dict(host="mongo", username="root", password="secret")),
    ],
)
def store(request):
    """This function instantiates a Store class."""
    StoreClass, kwargs = request.param
    return StoreClass(**kwargs)


class TestStore(object):
    @pytest.fixture(autouse=True)
    def setup(self, request, store):
        """This function inject the store fixture into the class
        via `@pytest.fixture(autouse=True)`

        """
        log.warning("Store class: %r", store.__class__)
        self.store = store
        self.store.add("1", {"1": 1})
        self.store.add("r", {"r": "r"})

    def test_add(self):
        i = {"2": 2}
        self.store.add("2", i)
        assert self.store.get("2") == i

    def test_remove(self):
        self.store.remove("r")
        assert self.store.get("r") is None

    def test_get(self):
        assert self.store.get("1") == {"1": 1}
        assert self.store.get("missing") is None

    def test_list(self):
        assert "1" in self.store.list()
