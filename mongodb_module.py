import global_parameters as g


class EditNotify:
    @staticmethod
    def create(notify: dict, **kwargs):
        g.ConnectMongo.for_update.get_collection(g.DB.notifications).insert_one(notify)
        del notify[g.KV.db_id]

    @staticmethod
    def delete(uuid: str, **kwargs):
        g.ConnectMongo.for_update.get_collection(g.DB.notifications).delete_one({g.KV.uuid: uuid})

    @staticmethod
    def update(uuid: str, data: dict):
        g.ConnectMongo.for_update.get_collection(g.DB.notifications).update_one({g.KV.uuid: uuid}, {'$set': data})


class GetNotify:
    @staticmethod
    def get_one(as_read: bool = None):
        ...

    @staticmethod
    def get_all(as_read: bool = None):
        ...

    @staticmethod
    def get_all_only_uuid() -> list:
        pipeline = [{'$match': {g.KV.uuid: {'$exists': True}}},
                    {'$group': {g.KV.db_id: None,
                                g.KV.uuid: {'$addToSet': '$' + g.KV.uuid}}},
                    {'$project': {g.KV.uuid: 1,
                                  g.KV.db_id: 0}}]
        return g.ConnectMongo.for_update.get_collection(g.DB.notifications).aggregate(pipeline).next()[g.KV.uuid]


class CreateUser:
    @staticmethod
    def first_request(token_cookie: str):
        filter_ = {g.KV.uuid: token_cookie}
        data = {g.KV.uuid: token_cookie,
                g.KV.notifications: [{g.KV.uuid: uuid, g.KV.is_read: False} for uuid in GetNotify.get_all_only_uuid()]}
        g.ConnectMongo.for_update.get_collection(g.DB.users).update_one(filter_, {'$set': data}, upsert=True)
