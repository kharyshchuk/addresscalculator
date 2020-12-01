from pymongo import MongoClient

from db_layers.common import get_mongo_connect_string, get_name_db
from db_layers.result_repository import ResultRepository


class DBLayer:
    def __init__(self):
        mongo_client = MongoClient(
            get_mongo_connect_string(),
        )
        self.db = mongo_client[get_name_db()]
        self._result_repository = None

    @property
    def result_repository(self):
        if not self._result_repository:
            self._result_repository = ResultRepository(self.db)

        return self._result_repository


db_mongo = DBLayer()

