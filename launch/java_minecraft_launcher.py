from os import remove, system, makedirs
from os.path import join, exists
from typing import Callable, Any
import platform
from minecraft_launch.modules.arguments_builders.java_minecraft_arguments_builder import JavaMinecraftArgumentsBuilder
from minecraft_launch.modules.enum.launch_state import LaunchState
from minecraft_launch.modules.interface.launcher_base import LauncherBase
from minecraft_launch.modules.models.launch.game_core import GameCore
from minecraft_launch.modules.models.launch.launch_config import LaunchConfig
from minecraft_launch.modules.models.launch.minecraft_launch_response import MinecraftLaunchResponse
from minecraft_launch.modules.utils.game_core_util import GameCoreUtil
from minecraft_launch.modules.utils.zip_util import ZipUtil


class JavaMinecraftLauncher(LauncherBase[JavaMinecraftArgumentsBuilder, MinecraftLaunchResponse]):
    @property
    def __system_dict(self) -> dict[str, str]:
        return {"Windows": ".bat", "Darwin": ".sh", "Linux": ".sh"}

    def __init__(self, launch_setting: LaunchConfig, game_core_toolkit: GameCoreUtil) -> None:
        self.launch_setting = launch_setting
        self.game_core_toolkit = game_core_toolkit
        makedirs(join("MLP", "shell")) if not exists(join("MLP", "shell")) else ...

    def launch(self, id: str, action: Callable[[tuple[float, str]], Any]|None = None) -> MinecraftLaunchResponse:
        # 预启动检查
        core: GameCore = self.game_core_toolkit.get_game_core(id)

        action((0.2, "正在查找游戏核心")) if action != None else ...
        if(core == None):
            action((float(-1), "启动失败,游戏核心不存在或已损坏")) if action != None else ...
            return MinecraftLaunchResponse(LaunchState.Failed, None, Exception("启动失败,游戏核心不存在或已损坏"))
        
        action((0.4, "正在检查 Jvm 配置")) if action != None else ...
        if(self.launch_setting.jvm_config == None):
            action((float(-1), "启动失败,未配置 Jvm 信息")) if action != None else ...
            return MinecraftLaunchResponse(LaunchState.Failed, None, Exception("启动失败，未配置 Jvm 信息"))

        if(not exists(self.launch_setting.jvm_config.java_path)):
            action((float(-1), "启动失败,Java 路径不存在或已损坏")) if action != None else...
            return MinecraftLaunchResponse(LaunchState.Failed, None, Exception("启动失败,Java 路径不存在或已损坏"))
        
        action((0.5, "正在验证账户信息")) if action != None else ...
        if(self.launch_setting.account == None):
            action((float(-1), "启动失败,未设置账户")) if action != None else ...
            return MinecraftLaunchResponse(LaunchState.Failed, None, Exception("启动失败,未设置账户"))
        
        action((0.6, "正在检查游戏依赖文件")) if action != None else ...
        
        action((0.8, "正在构建启动参数")) if action != None else ...
        self.arguments_builder = JavaMinecraftArgumentsBuilder(core, self.launch_setting)
        args = self.arguments_builder.build()

        action((0.9, "正在检查Natives")) if  action != None else ...
        if (self.launch_setting.natives_folder != None):
            if(exists(self.launch_setting.natives_folder)):
                natives: str = self.launch_setting.natives_folder 
        else:
            natives = join(core.root, "versions", core.id, "natives")

        ZipUtil.game_natives_decompress(natives, core.library_resources)

        # 启动
        action((1.0, "正在尝试启动游戏")) if action != None else ...
        shell = join("MLP", "shell", f"launch_process{self.__system_dict[platform.system()]}")
        bat = open(shell, "w")
        bat.write(str.join(" ", args))
        bat.close()
        system(shell)
        remove(shell)
        return MinecraftLaunchResponse(LaunchState.Success, args)