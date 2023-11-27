# this statement equals the declaration of all static parameters in the application
# further, all categories of global static parameters will be separated by headings
####################################################################################################################
import os
import binascii

from flask import request
from pymongo import MongoClient
from json import dumps as dm

from encryptor import Aes, load_app_api_key
from time_module import now_time_in_int as time_int


class KV:
    """name's value's (global key's)"""
    uuid = 'uuid'
    db_id = '_id'
    token = 'auth'
    token_ua = 'ua'
    token_a = 'a'
    token_sp = 'sp'
    token_hu = 'hu'
    token_ae = 'ae'
    token_sn = 'sn'
    system_title = 'system_title'
    system_description = 'system_description'
    notifications = 'notifications'
    date_create = 'date_create'
    date_update = 'date_update'

    frontend_cache_control = 'Cache-Control'
    frontend_cache_control_types = ['no-cache', 'no-store', 'public', 'private']
    host_url = 'http://127.0.0.1:19008/'

    def __setattr__(self, *args, **kwargs): raise NotImplementedError('can\'t rewrite attributes')

    def __delete__(self, instance): raise NotImplementedError('it is not possible to delete this configuration class of an application')

    def __delattr__(self, item): raise NotImplementedError('it is not possible to delete this configuration class of an application')


class DB:
    """Name's,

       Model's,

       Limit's

       and Other's (e.t.c.)

       for the all data base.
    """
    db_name = 'notify_center'
    localhost = '127.0.0.1'
    mongo_port = 58999

    # names collection's
    notifications = 'notifications'
    users = 'users'

    # limit's
    len_uuid = 32
    min_len_system_title = 1
    max_len_system_title = 128
    min_len_system_description = 1
    max_len_system_description = 512

    # model's
    @staticmethod
    def create_notify(system_title: str, system_description: str, **kwargs):
        result_model = {**kwargs}
        if isinstance(system_title, str):
            if DB.min_len_system_title <= len(system_title) <= DB.max_len_system_title:
                result_model[KV.system_title] = system_title
            else:
                return None
        else:
            return None
        if isinstance(system_description, str):
            if DB.min_len_system_description <= len(system_description) <= DB.max_len_system_description:
                result_model[KV.system_description] = system_description
            else:
                return None
        else:
            return None
        try:
            dm(result_model)  # check serialazing
        except (TypeError, OverflowError):
            return None
        result_model[KV.date_create] = time_int()
        result_model[KV.date_update] = None
        result_model[KV.uuid] = gen_sm_name()
        return result_model

    @staticmethod
    def create_token_cookie():
        """Create token-cookie.

        :return: str len 96 symbol's = [random + model_token]
        """
        model_token = {KV.token_ua: request.environ['HTTP_USER_AGENT'],
                       KV.token_a: request.environ['HTTP_ACCEPT'],
                       KV.token_sp: request.environ['SERVER_PROTOCOL'],
                       KV.token_ae: request.environ['HTTP_ACCEPT_ENCODING'],
                       KV.token_sn: request.environ['SERVER_NAME'],
                       KV.token_hu: request.host_url}
        return gen_sm_name() + Aes.get_hash_obj(model_token)

    def __setattr__(self, *args, **kwargs): raise NotImplementedError('can\'t rewrite attributes')
    def __delete__(self, instance): raise NotImplementedError('it is not possible to delete this configuration class of an application')
    def __delattr__(self, item): raise NotImplementedError('it is not possible to delete this configuration class of an application')


class RulesRoutes:
    """all rule's route's"""
    create_notify = '/api/v1/create_notify'
    delete_notify = '/api/v1/delete_notify'
    update_notify = '/api/v1/update_notify'
    get_one_notify = '/api/v1/get_one_notify'
    get_all_notify = '/api/v1/get_all_notify'

    def __setattr__(self, *args, **kwargs): raise NotImplementedError('can\'t rewrite attributes')
    def __delete__(self, instance): raise NotImplementedError('it is not possible to delete this configuration class of an application')
    def __delattr__(self, item): raise NotImplementedError('it is not possible to delete this configuration class of an application')


class ConnectMongo:
    for_update = MongoClient(DB.localhost,
                             port=DB.mongo_port,
                             socketTimeoutMS=300000,
                             connectTimeoutMS=300000,
                             serverSelectionTimeoutMS=300000,
                             waitQueueTimeoutMS=300000,
                             maxpoolsize=None,
                             waitQueueMultiple=None).get_database(DB.db_name)
    for_user = MongoClient(DB.localhost,
                           port=DB.mongo_port,
                           socketTimeoutMS=55000,
                           connectTimeoutMS=55000,
                           serverSelectionTimeoutMS=55000,
                           waitQueueTimeoutMS=55000,
                           maxpoolsize=None,
                           waitQueueMultiple=None).get_database(DB.db_name)

    def __setattr__(self, *args, **kwargs): raise NotImplementedError('can\'t rewrite attributes')
    def __delete__(self, instance): raise NotImplementedError('it is not possible to delete this configuration class of an application')
    def __delattr__(self, item): raise NotImplementedError('it is not possible to delete this configuration class of an application')


# initialization classes and update locale file's
KV = KV()
DB = DB()
ConnectMongo = ConnectMongo()
RulesRoutes = RulesRoutes()
Aes = Aes()
SpecialApiKey = load_app_api_key()  # return encrypted special only api key


def gen_sm_name(_len: int = 32) -> str:
    """return random symbols, len = _len"""
    return binascii.hexlify(os.urandom(_len)).decode('ascii')[:_len]
