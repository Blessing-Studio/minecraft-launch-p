from minecraft_launch.modules.models.auth.account import Account
from minecraft_launch.modules.models.launch.game_window_config import GameWindowConfig
from minecraft_launch.modules.models.launch.jvm_config import JvmConfig
from minecraft_launch.modules.models.launch.sever_config import SeverConfig


class LaunchConfig():
    def __init__(self, account: Account, 
                jvm_config: JvmConfig, 
                game_window_config: GameWindowConfig = GameWindowConfig(), 
                sever_config: SeverConfig|None = None, is_enable_independency_core: bool = True, 
                natives_folder: str|None = None, 
                working_folder: str|None = None):
        
        self.account: Account = account
        self.jvm_config: JvmConfig = jvm_config
        self.game_window_config: GameWindowConfig = game_window_config
        self.server_config = sever_config
        self.natives_folder: str|None = natives_folder
        self.working_folder: str|None = working_folder
        self.launch_name: str = "minecraft-launch-p"
        self.is_server: bool = True
        self.is_enable_independency_core: bool = is_enable_independency_core