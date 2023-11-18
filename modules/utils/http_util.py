from requests import get



class HttpUtil():
    @staticmethod
    def get_str(uri: str):
        return get(uri).json()