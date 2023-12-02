import global_parameters as g
from json import loads as ld


class EditNotify:
    @staticmethod
    def create(notify: dict):
        g.ConnectMongo.for_update.get_collection(g.DB.notifications).insert_one(notify)
        del notify[g.KV.db_id]

    @staticmethod
    def delete(uuid: str):
        g.ConnectMongo.for_update.get_collection(g.DB.notifications).delete_one({g.KV.uuid: uuid})

    @staticmethod
    def update(uuid: str, data: dict):
        g.ConnectMongo.for_update.get_collection(g.DB.notifications).update_one({g.KV.uuid: uuid}, {'$set': data})


class GetNotify:
    @staticmethod
    def get_one(uuid: str, token_cookie: str, **kwargs):
        params = {g.KV.uuid: uuid}
        filter_ = {g.KV.db_id: 0,
                   g.KV.system_title: 0,
                   g.KV.system_description: 0}
        notify = g.ConnectMongo.for_user.get_collection(g.DB.notifications).find(params, filter_).next()
        g.ConnectMongo.for_user.get_collection(g.DB.users).update_one({g.KV.uuid: token_cookie, f'{g.KV.notifications}.{g.KV.uuid}': uuid},
                                                                      {'$set': {f'{g.KV.notifications}.$.{g.KV.is_read}': True}}, upsert=True)
        return notify

    @staticmethod
    def get_all(token_cookie: str, as_read: bool = None, **kwargs):
        params = [{'$match': {g.KV.uuid: {'$exists': True}}},
                  {'$group': {g.KV.db_id: None,
                              g.KV.notifications: {'$push': {'$arrayToObject': {'$filter': {'input': {'$objectToArray': '$$ROOT'},
                                                                                            'as': 'field',
                                                                                            'cond': {'$and': [{'$ne': ['$$field.k', g.KV.db_id]},
                                                                                                              {'$ne': ['$$field.k', g.KV.system_title]},
                                                                                                              {'$ne': ['$$field.k', g.KV.system_description]}]}}}}}}},
                  {'$lookup': {'from': g.DB.users,
                               'let': {g.KV.uuid: token_cookie},
                               'pipeline': [{'$match': {'$expr': {'$eq': [f'${g.KV.uuid}', f'$${g.KV.uuid}']}}},
                                            {'$project': {g.KV.db_id: 0,
                                                          g.KV.notifications: 1}}],
                               'as': g.KV.reading_notifications}},
                  {'$unwind': f'${g.KV.reading_notifications}'},
                  {'$project': {g.KV.db_id: 0,
                                g.KV.notifications: 1,
                                g.KV.reading_notifications: f'${g.KV.reading_notifications}.{g.KV.notifications}'}}]
        if as_read is not None:
            if isinstance(as_read, str):
                if ld(as_read) is True:
                    flag = True
                else:
                    flag = False
            else:
                flag = as_read
            params[-1]['$project'][g.KV.reading_notifications] = {'$filter': {'input': f'${g.KV.reading_notifications}.{g.KV.notifications}',
                                                                              'as': g.KV.notifications,
                                                                              'cond': {'$eq': [f'$${g.KV.notifications}.{g.KV.is_read}', flag]}}}
        return g.ConnectMongo.for_user.get_collection(g.DB.notifications).aggregate(params).next()

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
