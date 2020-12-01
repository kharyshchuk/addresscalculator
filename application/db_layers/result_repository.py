import pymongo

from db_layers._mongo_base_repositories import BaseRepository

COLLECTION_NAME = "results"
RESULT_ID = 'result_id'


class ResultRepository(BaseRepository):

    def __init__(self, db):
        super(ResultRepository, self).__init__(
            db,
            collection_name=COLLECTION_NAME,
            index=[
                (RESULT_ID, pymongo.ASCENDING)
            ]
        )

    async def update_one(self, data):
        return await self.update(data)

    async def update(self, data):
        """
        :type alpha3: str
        """
        id = data.pop('_id')
        update_obj = await self.collection.update_one(filter={'_id': id}, update={"$set": data}, upsert=True)
        if update_obj.acknowledged:
            return await self.collection.find_one({'_id': id})
        else:
            return None

    async def find_one(self, result_id=None, without_id=False, *args, **kwargs):
        params = ResultRepository._prepare_params(result_id=result_id)
        return await super(ResultRepository, self).find_one(params, without_id=without_id)

    @staticmethod
    def _prepare_params(result_id=None):
        params = {}
        if result_id:
            params[RESULT_ID] = result_id

        return params
