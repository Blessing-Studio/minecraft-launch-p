from minecraft_launch.modules.models.install.installer_response_base import InstallerResponseBase
from minecraft_launch.modules.models.launch.game_core import GameCore


class InstallerResponse(InstallerResponseBase):
    def __init__(self):
        self.game_core: GameCore