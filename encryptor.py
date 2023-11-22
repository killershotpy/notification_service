from random import choices as cho
from hashlib import sha512 as sha_512, sha256 as sha_256
from typing import Any as Any
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from os import urandom as ur, path as pt
from json import loads as ld, dumps as dm


class Aes:
    def __init__(self, key: bytes = None):
        self.e_key = sha_256(key).digest() if key else sha_256(load_app_key()).digest()
        self.dump_json = dm
        self.load_json = ld

    def encrypt(self, obj: Any) -> bytes:
        """Encrypting any object's, that can serialized JSON standard.

        :param obj: Any object, that it's can serialized JSON standard.
        :return: Bytes string encrypt by algorithm AES_256, [obj: bytes].
        """

        enc = Cipher(algorithms.AES(self.e_key), modes.OFB(self.e_key[:16]), default_backend()).encryptor()
        return self.e_key[:16] + enc.update(self.pad(dm(obj)).encode('utf-8')) + enc.finalize()

    def decrypt(self, c_obj: bytes = None) -> Any:
        """Decrypt encrypted object and return serialized JSON standard object.

        :param c_obj: encrypted object
        :return: JSON structured object
        """
        dec = Cipher(algorithms.AES(self.e_key), modes.OFB(c_obj[:16]), default_backend()).decryptor()
        s = (dec.update(c_obj[16:]) + dec.finalize()).decode('utf-8')
        return ld(s[:-ord(s[len(s) - 1:])])

    @staticmethod
    def pad(s: str) -> str:
        padding = (16 - (len(s) % 16))
        return s + padding * chr(padding)

    @staticmethod
    def get_hash_obj(obj: Any, _len: int = 64) -> str:
        return sha_512(dm(obj).encode('utf-8')).hexdigest()[:_len]


def generate_app_key(length: int = 256, path_key: str = 'key'):
    """Generate bytes by os.urandom() (default 256) and save on (this) work directory.

    key - is name file because saved.

    :param path_key: absolute path to secret key app
    :param length: key length after generation in bytes
    :return: None
    """
    if not pt.exists(path_key):
        open(path_key, 'wb').write(ur(length))


def load_app_key(path_key: str = 'key'):
    """Load secret key app.

    Return object type bytes.

    :param path_key: absolute path to secret key app
    :return: byte string
    """
    try:
        return open(path_key, 'rb').read()
    except FileNotFoundError:
        generate_app_key(path_key=path_key)
        return open(path_key, 'rb').read()


def generate_app_api_key(length: int = 32, path_api_key: str = 'api_key'):
    """Generate str by random 32 symbols in latin-1 (default 32) and save on (this) work directory.

    key - is name file because saved.

    :param path_api_key: absolute path to only special api_key app
    :param length: key length after generation in str
    :return: None
    """
    if not pt.exists(path_api_key):
        key = gen_sm_name(length)
        print(key)
        open(path_api_key, 'wb').write(Aes(load_app_key()).encrypt(key))


def load_app_api_key(path_api_key: str = 'api_key'):
    """Load only special api_key app.

        Return object type bytes.

        :param path_api_key: absolute path to only special api_key app
        :return: encrypted special api_key in byte string
    """
    try:
        return open(path_api_key, 'rb').read()
    except FileNotFoundError:
        generate_app_api_key(path_api_key=path_api_key)
        return open(path_api_key, 'rb').read()


def gen_sm_name(_len: int) -> str:
    """return random symbols, len = _len"""
    symbols = ['q', 'Q', 'w', 'W', 'e', 'E', 'r', 'R', 't', 'T', 'y', 'Y', 'u', 'U', 'i', 'I', 'o', 'O', 'p', 'P', 'a', 'A', 's', 'S', 'd', 'D', 'f', 'F', 'g', 'G', 'h', 'H', 'j', 'J', 'k', 'K', 'l', 'L', 'z', 'Z', 'x', 'X', 'c', 'C', 'v', 'V', 'b', 'B', 'n', 'N', 'm', 'M', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    return ''.join(cho(symbols, k=_len))
