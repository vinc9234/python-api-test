class Store(object):
    """
    This is a store implemented via a dict().
    What can go wrong here?
    Implement some tests, then fix the code.
    """

    def __init__(self, **kwargs):
        """Initialize store"""
        self._store = dict()

    def ping(self):
        return isinstance(self._store, dict)

    def add(self, key, value):
        self._store[key] = value

    def remove(self, key):
        if key in self._store:
            del self._store[key]

    def list(self, cursor: str = None):
        if cursor:
            return {k: v for k, v in self.store if k > cursor}
        return self._store

    def get(self, key):
        return self._store.get(key, None)


from pymongo import MongoClient
from pymongo.errors import PyMongoError


class MongoStore(object):
    """
    This store forwards objects to mongodb.

    Check this class carefully.
    What can go wrong here?
    Implement some tests, then fix the code.
    """

    def __init__(self, **kwargs):
        self.client = MongoClient(**kwargs)
        self._store = self.client["db"]["collection"]

    def ping(self):
        try:
            ret = self._store.find_one()
            return ret is not None
        except PyMongoError:
            return False

    def add(self, key: str, value):
        e = {"_id": key, "v": value}
        return self._store.replace_one({"_id": key}, e, upsert=True)

    def remove(self, key: str):
        return self._store.delete_one(dict(_id=key))

    def get(self, key: str):
        res = self._store.find_one(dict(_id=key))
        if res:
            return res["v"]

    def list(self, cursor: str = None):
        f = {"_id": {"$gt": cursor}} if cursor else {}
        q = [{"$match": f}]  # , {"$replaceRoot": {"newRoot": "$v"}}]
        return {q["_id"]: q["v"] for q in self._store.aggregate(q)}
