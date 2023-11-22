# this statement equals the declaration of all static parameters in the application
# further, all categories of global static parameters will be separated by headings
####################################################################################################################
import os
import binascii
import requests

from pymongo import MongoClient
from redis import ConnectionPool, Redis
from json import dump as dp, loads as ld
from json.decoder import JSONDecodeError
from email._parseaddr import AddressList as check_email

from encryptor import Aes, load_app_api_key
from time_module import now_time_in_int as time_int


class KV:
    """name's value's (global key's)"""
    token = 'auth'
    token_ua = 'ua'
    token_a = 'a'
    token_sp = 'sp'
    token_hu = 'hu'
    token_ae = 'ae'
    token_sn = 'sn'
    token_hash = 'hash'
    token_nonce = 'n'
    token_ttd = 'ttd'
    rejected_ttd_p = 'ttd_p'
    email = 'email'
    uuid = 'uuid'
    api_key = 'api_key'
    plug_api_key = '0000000000'
    type_p = 'type'
    date_create_p = 'date_create'
    date_closed_p = 'date_closed'
    zh_p = 'zh'
    es_p = 'es'
    en_p = 'en'
    ru_p = 'ru'
    language_p = 'lang'
    languages_p = [zh_p, es_p, ru_p, en_p]
    default_image_p = 'https://wm3d.com/image.png'
    db_id = '_id'
    url_path_from_robots = 'url_path'
    email_subject = 'subject'
    email_from = 'from'
    email_to = 'to'
    email_path_to_temp = 'path_to_temp'
    og_keywords = 'keywords'
    og_keywords_lang = {en_p: 'Interface Design,Web Design,Adaptive design,Graphic design,Figma,User interface design,UX,UX UI,UX design,Design',
                        es_p: 'Diseño de Interfaces,Diseño Web,Diseño adaptativo,Diseño gráfico,figma,diseño de interfaz de usuario,experiencia de usuario,UX UI,diseño de experiencia de usuario,Diseño,Interfaz',
                        ru_p: 'Дизайн интерфейсов,Веб-дизайн,Адаптивный дизайн,Графический дизайн,Figma,UI дизайн,UX,UX UI,UX дизайн,Дизайн,Интерфейс',
                        zh_p: '界面设计,网页设计 ,适应性设计,平面設計,菲格瑪,用戶界面設計,用戶體驗,用戶體驗用戶界面,用戶體驗設計,設計'}
    private_fields_for_logger = [db_id, email]

    collection_zh = 'wm3d_zh'  # !!! this name - names the collection
    collection_es = 'wm3d_es'  # !!! this name - names the collection
    collection_ru = 'wm3d_ru'  # !!! this name - names the collection
    collection_en = 'wm3d_en'  # !!! this name - names the collection
    map_lang_collection = {zh_p: collection_zh,
                           es_p: collection_es,
                           ru_p: collection_ru,
                           en_p: collection_en}

    captcha = 'captcha'
    captcha_answer = 'answer'
    captcha_math = {'+': int.__add__,
                    '-': int.__sub__,
                    '*': int.__mul__}

    frontend_cache_control = 'Cache-Control'
    frontend_cache_control_types = ['no-cache', 'no-store', 'public', 'private']
    frontend_cache_control_default = [2, 43200]

    def __setattr__(self, *args, **kwargs): raise NotImplementedError('can\'t rewrite attributes')
    def __delete__(self, instance): raise NotImplementedError('it is not possible to delete this configuration class of an application')
    def __delattr__(self, item): raise NotImplementedError('it is not possible to delete this configuration class of an application')


class PathNames:
    """different way's to work"""
    current_app = os.getcwd()
    tg_bot_api_token = ''
    tg_chat_notify_id = ''
    google_captcha_secret_key = ''
    list_current_domains = ['http://127.0.0.1:19008/', 'http://127.0.0.1:5000/', 'https://wm3d.com']
    dir_templates = f'{current_app}{os.sep}templates'
    file_favicon_ico = f'{current_app}{os.sep}static{os.sep}favicon.ico'
    dir_to_sitemap = f'{dir_templates}{os.sep}sitemap'
    dir_translates = f'{current_app}{os.sep}translates'
    if os.path.exists(f'{current_app}{os.sep}static{os.sep}fonts{os.sep}roboto{os.sep}times.ttf'):
        path_file_standard_font = f'{current_app}{os.sep}static{os.sep}fonts{os.sep}roboto{os.sep}times.ttf'
    else:
        path_file_standard_font = None
    info_email = ''
    media_email = ''
    support_email = ''
    tech_email = ''

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
    db_name = 'wm3d'
    localhost = '127.0.0.1'
    mongo_port = 58999
    redis_port = 58995

    # names collection's
    users = 'users'
    tokens_admin = 'tokens_admin'
    tokens_other = 'tokens_other'
    logging_admins = 'logging_admins'
    collection_zh = KV.collection_zh
    collection_es = KV.collection_es
    collection_ru = KV.collection_ru
    collection_en = KV.collection_en

    # limit's
    len_uuid = 32
    len_email_min = 6  # RFC 3696
    len_email_max = 320  # RFC 3696 - Section 3

    # model's
    @staticmethod
    def create_model_token(uuid: str = None,
                           request=None,
                           create_token: bool = None,
                           check_token: bool = None,
                           **kwargs):
        """Create or update_updates model token auth.

        :param uuid: uuid the account
        :param role: role this account
        :param lvl_access: lvl access this account
        :param request: object current connection [flask.request]
        :param create_token: if True, add inside the model hash of the result of this model (sha512), key = 'hash_'
        :param check_token: if True, return only hash model_token, for check in data base tokens
        :return: hash string of the final object in the database, len (128 symbols) and model token object
        """
        model_token = {KV.uuid: uuid,
                       KV.token_ua: request.environ['HTTP_USER_AGENT'],
                       KV.token_a: request.environ['HTTP_ACCEPT'],
                       KV.token_sp: request.environ['SERVER_PROTOCOL'],
                       KV.token_ae: request.environ['HTTP_ACCEPT_ENCODING'],
                       KV.token_sn: request.environ['SERVER_NAME'],
                       KV.token_hu: request.host_url}
        if check_token:
            return Aes.get_hash_obj(model_token)
        hash_ = Aes.get_hash_obj(model_token)
        if create_token:
            # current hash + 32 symbol's from [gen_sm_name()]
            model_token[KV.token_nonce] = gen_sm_name()
            hash_ += model_token[KV.token_nonce]
        return [hash_, model_token]


    def __setattr__(self, *args, **kwargs): raise NotImplementedError('can\'t rewrite attributes')
    def __delete__(self, instance): raise NotImplementedError('it is not possible to delete this configuration class of an application')
    def __delattr__(self, item): raise NotImplementedError('it is not possible to delete this configuration class of an application')


class RulesRoutes:
    """all rule's route's"""
    main = '/'
    main_og = '/<string(length=2):lang>/<string(length=32):uuid>'
    main_og_robots = '/<string(length=6):robots>/<string(length=2):lang>/<string(length=32):uuid>'
    api_get_updates = '/api/v1/get_updates'
    api_get_captcha = '/api/v1/get_captcha'
    api_get_total_pub_and_lang = '/api/v1/stat_server'

    def __setattr__(self, *args, **kwargs): raise NotImplementedError('can\'t rewrite attributes')
    def __delete__(self, instance): raise NotImplementedError('it is not possible to delete this configuration class of an application')
    def __delattr__(self, item): raise NotImplementedError('it is not possible to delete this configuration class of an application')


class PagesNames:
    """name page's .html"""
    main_users = 'main_users.html'
    main_robots = 'main_robots.html'
    main_admin = 'main_admin.html'
    main_mentor = 'main_mentor.html'

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


class ConnectRedis:
    pool = ConnectionPool(host=DB.localhost, port=DB.redis_port, db=0, socket_connect_timeout=15, socket_timeout=15)

    def connect(self):
        return Redis(connection_pool=self.pool)

    def __setattr__(self, *args, **kwargs): raise NotImplementedError('can\'t rewrite attributes')
    def __delete__(self, instance): raise NotImplementedError('it is not possible to delete this configuration class of an application')
    def __delattr__(self, item): raise NotImplementedError('it is not possible to delete this configuration class of an application')


# initialization classes and update locale file's
Test = False  # testing functions, if True, or False = off test lines of code
KV = KV()
PathNames = PathNames()
DB = DB()
ConnectMongo = ConnectMongo()
ConnectRedis = ConnectRedis()
RulesRoutes = RulesRoutes()
PagesNames = PagesNames()
Aes = Aes()
SpecialApiKey = load_app_api_key()  # return encrypted special only api key

# normalization symbol's
rs_symbols = str.maketrans({"!": None, "@": None, "#": None, "№": None, "$": None, ";": None, "%": None, "^": None, ":": None, "&": None, "?": None, "*": None, "(": None, ")": None, "=": None, "+": None, "{": None, "}": None, "[": None, "]": None, "\"": None, "\'": None, "<": None, ">": None, "|": None, "\\": None, "/": None, ",": None, ".": None, "~": None, "`": None, " ": None, " ": None})
rs_symbols_easy = str.maketrans({"!": None, "@": None, "#": None, "№": None, "$": None, ";": None, "%": None, "^": None, ":": None, "&": None, "?": None, "*": None, "=": None, "+": None, "{": None, "}": None, "[": None, "]": None, "\"": None, "\'": None, "<": None, ">": None, "|": None, "\\": None, "/": None, ",": None, ".": None, "~": None, "`": None})


def gen_sm_name(_len: int = 32) -> str:
    """return random symbols, len = _len"""
    return binascii.hexlify(os.urandom(_len)).decode('ascii')[:_len]


def bot_notify(message: str):
    while True:
        try:
            requests.post(f'https://api.telegram.org/bot{PathNames.tg_bot_api_token}/sendMessage?chat_id={PathNames.tg_chat_notify_id}', data={'text': f'{message}'})
            break
        except requests.exceptions.ConnectTimeout:
            pass
