from minecraft_launch.modules.enum.account_type import AccountType
from uuid import uuid4


class OfflineAccount():
    def __init__(self, 
                name: str,
                uuid: str = uuid4(), 
                access_token: str = uuid4().hex, 
                client_token: str = uuid4().hex):
        self.uuid = uuid
        self.access_token = access_token
        self.client_token = client_token
        self.name = name
        self.type = AccountType.Offline
