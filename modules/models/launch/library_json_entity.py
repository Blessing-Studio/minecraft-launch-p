from modules.models.download.downloads_json_entity import DownloadsJsonEntity
from modules.models.launch.rule_entity import RuleEntity


class LibraryJsonEntity():
    def __init__(self): 
        self.downloads: DownloadsJsonEntity
        self.name: str
        self.url: str
        self.natives: dict[str, str]
        self.rules: list[RuleEntity]
        self.check_sum: list[str]
        self.client_req: bool
