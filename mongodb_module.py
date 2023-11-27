import global_parameters as g


class EditNotify:
    @staticmethod
    def create(notify: dict):
        g.ConnectMongo.for_update.get_collection(g.DB.notifications).insert_one(notify)
        del notify[g.KV.db_id]

    @staticmethod
    def delete(uuid: str):
        ...

    @staticmethod
    def update(uuid: str, data: dict):
        ...


class GetNotify:
    @staticmethod
    def get_one(as_read: bool = None):
        ...

    @staticmethod
    def get_all(as_read: bool = None):
        ...
