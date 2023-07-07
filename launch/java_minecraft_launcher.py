from os import remove, system
import platform
from modules.arguments_builders.java_minecraft_arguments_builder import JavaMinecraftArgumentsBuilder
from modules.models.launch.launch_config import LaunchConfig
from modules.toolkits.game_core_toolkit import GameCoreToolkit


class JavaMinecraftLauncher():
    def __init__(self, launch_setting: LaunchConfig, game_core_toolkit: GameCoreToolkit, enable_independency_core: bool = False):
        self.launch_setting = launch_setting
        self.game_core_toolkit = game_core_toolkit
        self.enable_indpendency_core = enable_independency_core

    def launch_task_async(self, id: str):
        __system_dict = {"Windows": ".bat", "Mac": ".sh", "Linux": ".sh"}
        arguments_builder = JavaMinecraftArgumentsBuilder(
            self.game_core_toolkit.root,
            id, 
            self.launch_setting.jvm_config[0], 
            self.launch_setting.jvm_config[1], 
            self.launch_setting.account, 
            self.launch_setting.game_window_config[0], 
            self.launch_setting.game_window_config[1])

        __shell = f"run{__system_dict[platform.system()]}"
        bat = open(__shell, "w")
        bat.write(arguments_builder.build())
        bat.close()
        system(__shell)
        remove(__shell)

    def launch(self, id: str):
        pass
