from requests import get
from json import loads

class HttpUtil():
    @staticmethod
    def get_str(uri: str):
        return get(uri).json()