from minecraft_launch.modules.enum.account_type import AccountType
from minecraft_launch.modules.models.auth.offline_account import OfflineAccount
from uuid import uuid4


class Account():
    default: OfflineAccount = OfflineAccount(
        name = "Steve",
        uuid = uuid4(),
        access_token = uuid4().hex,
        client_token = uuid4().hex
    )
    
    def __init__(self, name: str, uuid: str, access_token: str, client_token: str = None) -> None:
        self.type: AccountType
        self.name = name
        self.uuid = uuid
        self.access_token = access_token
        self.client_token = client_token