# this statement equals the declaration of all static parameters in the application
# further, all categories of global static parameters will be separated by headings
####################################################################################################################
import os
import binascii

from pymongo import MongoClient
from redis import ConnectionPool, Redis

from encryptor import Aes, load_app_api_key


class KV:
    """name's value's (global key's)"""
    uuid = 'uuid'
    db_id = '_id'
    system_title = 'system_title'
    notifications = 'notifications'
    frontend_cache_control = 'Cache-Control'
    frontend_cache_control_types = ['no-cache', 'no-store', 'public', 'private']

    def __setattr__(self, *args, **kwargs): raise NotImplementedError('can\'t rewrite attributes')
    def __delete__(self, instance): raise NotImplementedError('it is not possible to delete this configuration class of an application')
    def __delattr__(self, item): raise NotImplementedError('it is not possible to delete this configuration class of an application')


class PathNames:
    """different way's to work"""
    current_app = os.getcwd()

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

    # model's
    @staticmethod
    def first_def():
        ...

    def __setattr__(self, *args, **kwargs): raise NotImplementedError('can\'t rewrite attributes')
    def __delete__(self, instance): raise NotImplementedError('it is not possible to delete this configuration class of an application')
    def __delattr__(self, item): raise NotImplementedError('it is not possible to delete this configuration class of an application')


class RulesRoutes:
    """all rule's route's"""
    main = '/'

    def __setattr__(self, *args, **kwargs): raise NotImplementedError('can\'t rewrite attributes')
    def __delete__(self, instance): raise NotImplementedError('it is not possible to delete this configuration class of an application')
    def __delattr__(self, item): raise NotImplementedError('it is not possible to delete this configuration class of an application')


class PagesNames:
    """name page's .html"""
    default_page = 'default_page.html'

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
Test = False  # testing functions, if True, or False = off test lines of code
KV = KV()
PathNames = PathNames()
DB = DB()
ConnectMongo = ConnectMongo()
RulesRoutes = RulesRoutes()
PagesNames = PagesNames()
Aes = Aes()
SpecialApiKey = load_app_api_key()  # return encrypted special only api key


def gen_sm_name(_len: int = 32) -> str:
    """return random symbols, len = _len"""
    return binascii.hexlify(os.urandom(_len)).decode('ascii')[:_len]
