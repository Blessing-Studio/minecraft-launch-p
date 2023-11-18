from json import loads
from os.path import join
from typing import Iterable
from datetime import datetime
from minecraft_launch.modules.models.download.file_resource import FileResource
from minecraft_launch.modules.models.download.library_resource import LibraryResource
from minecraft_launch.modules.models.launch.mod_loader_info import ModLoaderInfo


class GameCore():
    def __init__(self) -> None:
        self.id: str
        self.root: str
        self.type: str
        self.main_class: str
        self.inherits_from: str|None = None
        self.java_version: int
        self.library_resources: list[LibraryResource]
        self.client_file: FileResource|None = None
        self.log_config_file: FileResource
        self.assets_index_file: FileResource
        self.behind_arguments: list[str] = []
        self.front_arguments: list[str]
        self.source: str
        self.has_mod_loader: bool
        self.mod_loader_infos: Iterable[ModLoaderInfo] = []

        # 用于获取不同path的方法
        self.get_versions_path = lambda : join(self.root, "versions")
        self.get_game_core_path = lambda isolate = True : join(self.get_versions_path() if isolate else self.root, self.id if isolate else "")
        self.get_options_file_path = lambda isolate = True : join(self.get_game_core_path(isolate), "options.txt") 

    def __eq__(self, obj: object) -> bool:
        if(hasattr(obj, "id")):
            return ((obj.id) == self.id)
        else: return False

    def __gt__(self, obj) -> bool:
        with open(join(self.root, "versions", self.id, f"{self.id}.json")) as f:
            json = loads(f.read())
            d1 = datetime.fromisoformat(json["releaseTime"])

        with open(join(obj.root, "versions", obj.id, f"{obj.id}.json")) as f:
            json = loads(f.read())
            d2 = datetime.fromisoformat(json["releaseTime"])

        return d1 > d2
        
    def __lt__(self, obj) -> bool:
        return not self.__gt__(obj)
    
    def __ne__(self, obj) -> bool:
        return not self.__eq__(obj)
    
    def __ge__(self, obj) -> bool:
        return (self.__gt__(obj) or self.__eq__(obj))
    
    def __le__(self, obj) -> bool:
        return (self.__lt__(obj) or self.__eq__(obj))