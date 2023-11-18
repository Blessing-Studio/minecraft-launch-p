from typing import Iterable
from minecraft_launch.modules.interface.iresource import IResource
from minecraft_launch.modules.models.launch.game_core import GameCore
from minecraft_launch.modules.utils.extend_util import ExtendUtil


class ResourceInstaller():
    max_download_threads: int = 64

    def __init__(self, game_core: GameCore) -> None:
        self.game_core: GameCore = game_core
        self.failed_resouces: list[IResource] = []

    def get_file_resources(self) -> Iterable[IResource]:
        if(self.game_core.client_file != None):
            yield self.game_core.client_file

    async def get_assets_resources_async(self):
        if(not(ExtendUtil.verify(self.game_core.assets_index_file.file_info, self.game_core.assets_index_file.size) or\
            ExtendUtil.verify(self.game_core.assets_index_file.file_info, self.game_core.assets_index_file.check_sum))):
            ...