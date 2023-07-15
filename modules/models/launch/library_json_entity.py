from modules.models.download.downloads_json_entity import DownloadsJsonEntity
from modules.models.launch.rule_entity import RuleEntity


class LibraryJsonEntity():
    downloads: DownloadsJsonEntity
    name: str
    url: str
    natives: dict[str, str]
    rules: list[RuleEntity]
    check_sum: list[str]
    client_req: bool
