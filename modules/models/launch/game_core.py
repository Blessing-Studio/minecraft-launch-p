from os.path import join
from typing import Iterable
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
        self.client_file: FileResource
        self.log_config_file: FileResource
        self.assets_index_file: FileResource
        self.behind_arguments: list[str] = []
        self.front_arguments: list[str]
        self.source: str
        self.has_mod_loader: bool
        self.mod_loader_infos: Iterable[ModLoaderInfo] = []

        self.get_versions_path = lambda : join(self.root, "versions")
        self.get_game_core_path = lambda isolate = True : join(self.get_versions_path() if isolate else self.root, self.id if isolate else "")
        self.get_options_file_path = lambda isolate = True : join(self.get_game_core_path(isolate), "options.txt") 
