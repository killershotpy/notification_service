from copy import deepcopy

import global_parameters as g


class LoggerDB:
    @staticmethod
    def write_log(action_admin: str,
                  time: str,
                  **kwargs):
        """Write object in data base, to the then get and reading.

        :param action_admin: action - reject, approve, delete or other's
        :param time: time in UTC format
        :param kwargs: other KV
        :return: None
        """
        params = {g.KV.action_admin: action_admin,
                  g.KV.time_action: str(time),
                  **{k: v for k, v in kwargs.items() if k not in g.KV.private_fields_for_logger}}
        g.ConnectMongo.for_update.get_collection(g.DB.logging_admins).insert_one(deepcopy(params))
        g.bot_notify(f'#{action_admin}\n\n' + '\n'.join([f'{n+1}. {k} | {v}' for n, (k, v) in enumerate(params.items())]))


class TokenAuth:
    @staticmethod
    def get(auth: str = None, **kwargs):
        """Find token in data base.

        :param auth: Hash [sha512] object token auth + 32 symbol's from [gen_sm_name()]
        :return: object token auth and other information of user
        """
        if auth:
            return g.ConnectRedis.connect().get(auth)
        else:
            return None

    @staticmethod
    def create(hash_: str, model_token: dict):
        g.ConnectRedis.connect().set(hash_, g.Aes.dump_json(model_token), g.DB.ttl_tokens[model_token[g.KV.role]])
        return hash_

    @staticmethod
    def update(token: str, model_token: dict):
        g.ConnectRedis.connect().delete(token)
        model_token[g.KV.token_nonce] = g.gen_sm_name()
        new_hash = token[:64] + model_token[g.KV.token_nonce]
        g.ConnectRedis.connect().set(new_hash, g.Aes.dump_json(model_token), g.DB.ttl_tokens[model_token[g.KV.role]])
        return new_hash

    @staticmethod
    def delete(auth: str = None, **kwargs):
        if auth:
            return g.ConnectRedis.connect().delete(auth)
        else:
            return None
