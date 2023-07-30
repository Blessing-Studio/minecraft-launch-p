from os import remove, system, makedirs
from os.path import join
import platform
from modules.arguments_builders.java_minecraft_arguments_builder import JavaMinecraftArgumentsBuilder
from modules.interface.launch_base import LaunchBase
from modules.models.launch.game_core import GameCore
from modules.models.launch.launch_config import LaunchConfig
from modules.models.launch.minecraft_launch_response import MinecraftLaunchResponse
from modules.utils.game_core_util import GameCoreUtil


class JavaMinecraftLauncher(LaunchBase[JavaMinecraftArgumentsBuilder, MinecraftLaunchResponse]):
    def __init__(self, launch_setting: LaunchConfig, game_core_toolkit: GameCoreUtil):
        self.launch_setting = launch_setting
        self.game_core_toolkit = game_core_toolkit

    def launch_task_async(self, id: str):
        try:
            makedirs(join("MLP", "shell"))
        except:
            ...

        core: GameCore = self.game_core_toolkit.get_game_core(id)

        __system_dict = {"Windows": ".bat", "Darwin": ".sh", "Linux": ".sh"}
        arguments_builder = JavaMinecraftArgumentsBuilder(
            core,
            self.launch_setting
            )

        __shell = join("MLP", "shell", f"launch{__system_dict[platform.system()]}")
        args = arguments_builder.build()
        bat = open(__shell, "w")
        bat.write(str.join(" ", args))
        bat.close()
        system(__shell)
        remove(__shell)

    def launch(self, id: str):
        pass
