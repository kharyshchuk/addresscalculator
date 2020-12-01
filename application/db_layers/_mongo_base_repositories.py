import pymongo


class BaseRepository:
    def __init__(self, db, collection_name, index=None, **kwargs):
        self.db = db
        self.collection = db[f"{collection_name}"]
        self.index = None
        norm_index = self._prepare_index(index)
        if norm_index:
            self.index = dict(norm_index)
            params = kwargs['index_param'] if 'index_param' in kwargs else {}
            self.collection.create_index(norm_index, **params)

    def _prepare_index(self, index, list_indexes=None, **kwargs):
        if index:
            if list_indexes is None:
                list_indexes = []
            if isinstance(index, dict):
                for k, v in iter(index):
                    self._prepare_index(index=tuple(k, v), list_indexes=list_indexes)
            elif isinstance(index, (set, list)):
                for i in index:
                    self._prepare_index(index=i, list_indexes=list_indexes)
            elif isinstance(index, str):
                list_indexes.append(tuple(index, pymongo.ASCENDING))
            else:
                list_indexes.append(index)
        return list_indexes

    async def save(self, data, upsert_mode=False):
        try:
            if '_id' in data:
                await self.collection.update_one({"_id": data['_id']}, {"$set": data}, upsert=upsert_mode)
                return await super(self.__class__, self).find_one(data)

            insert_obj = self.collection.insert_one(data)
            data.pop('_id')
            if insert_obj.acknowledged:
                return self.collection.find_one({'_id': insert_obj.inserted_id})
            else:
                return None
        except Exception as ex:
            print(ex.args[0])
            if ex.args[0] == 'not master':
                await self.save(data, upsert_mode)

    async def find_one(self, data, without_id=False):
        try:
            obj = self.collection.find_one(data)
            if without_id:
                obj.pop('_id', None)
            return obj
        except Exception as ex:
            print(f"{ex.args}")
            return None

    async def find(self, data, without_id=False):
        find_docs = []
        async for item in self.collection.find(data):
            if without_id:
                item.pop('_id', None)

            find_docs.append(item)
        return find_docs

    async def delete_one(self, data):
        return await self.collection.delete_one(data)

    async def delete_many(self, data):
        return await self.collection.delete_many(data)
