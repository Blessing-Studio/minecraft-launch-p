from os import remove, system, makedirs
from os.path import join, exists
import platform
from modules.arguments_builders.java_minecraft_arguments_builder import JavaMinecraftArgumentsBuilder
from modules.interface.launch_base import LaunchBase
from modules.models.launch.game_core import GameCore
from modules.models.launch.launch_config import LaunchConfig
from modules.models.launch.minecraft_launch_response import MinecraftLaunchResponse
from modules.utils.game_core_util import GameCoreUtil
from modules.utils.zip_util import ZipUtil


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

        __shell = join("MLP", "shell", f"launch_process{__system_dict[platform.system()]}")
        args = arguments_builder.build()

        if (self.launch_setting.natives_folder != None):
            if(exists(self.launch_setting.natives_folder)):
                natives: str = self.launch_setting.natives_folder 
        else:
            natives = join(core.root, "versions", core.id, "natives")

        ZipUtil.game_natives_decompress(natives, core.library_resources)

        bat = open(__shell, "w")
        bat.write(str.join(" ", args))
        bat.close()
        system(__shell)
        remove(__shell)

    def launch(self, id: str):
        pass
