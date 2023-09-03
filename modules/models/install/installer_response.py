from modules.models.install.installer_response_base import InstallerResponseBase
from modules.models.launch.game_core import GameCore


class InstallerResponse(InstallerResponseBase):
    def __init__(self):
        self.game_core: GameCore