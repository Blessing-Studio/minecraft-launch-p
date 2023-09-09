from os import remove, system, makedirs
from os.path import join, exists
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

    def __init__(self, launch_setting: LaunchConfig, game_core_toolkit: GameCoreUtil):
        self.launch_setting = launch_setting
        self.game_core_toolkit = game_core_toolkit
        makedirs(join("MLP", "shell")) if not exists(join("MLP", "shell")) else ...

    def launch(self, id: str, function = None) -> MinecraftLaunchResponse:
        # 预启动检查
        core: GameCore = self.game_core_toolkit.get_game_core(id)

        function((0.2, "正在查找游戏核心")) if function != None else ...
        if(core == None):
            function((-1, "启动失败,游戏核心不存在或已损坏")) if function != None else ...
            return MinecraftLaunchResponse(LaunchState.Failed, None, Exception("启动失败,游戏核心不存在或已损坏"))
        
        function((0.4, "正在检查 Jvm 配置")) if function != None else ...
        if(self.launch_setting.jvm_config == None):
            function((-1, "启动失败,未配置 Jvm 信息")) if function != None else ...
            return MinecraftLaunchResponse(LaunchState.Failed, None, Exception("启动失败，未配置 Jvm 信息"))

        if(not exists(self.launch_setting.jvm_config.java_path)):
            function((-1, "启动失败,Java 路径不存在或已损坏")) if function != None else...
            return MinecraftLaunchResponse(LaunchState.Failed, None, Exception("启动失败,Java 路径不存在或已损坏"))
        
        function((0.5, "正在验证账户信息")) if function != None else ...
        if(self.launch_setting.account == None):
            function((-1, "启动失败,未设置账户")) if function != None else ...
            return MinecraftLaunchResponse(LaunchState.Failed, None, Exception("启动失败,未设置账户"))
        
        function((0.6, "正在检查游戏依赖文件")) if function != None else ...
        
        function((0.8, "正在构建启动参数")) if function != None else ...
        self.arguments_builder = JavaMinecraftArgumentsBuilder(core, self.launch_setting)
        args = self.arguments_builder.build()

        function((0.9, "正在检查Natives")) if  function != None else ...
        if (self.launch_setting.natives_folder != None):
            if(exists(self.launch_setting.natives_folder)):
                natives: str = self.launch_setting.natives_folder 
        else:
            natives = join(core.root, "versions", core.id, "natives")

        ZipUtil.game_natives_decompress(natives, core.library_resources)

        # 启动
        function((1, "正在尝试启动游戏")) if function != None else ...
        shell = join("MLP", "shell", f"launch_process{self.__system_dict[platform.system()]}")
        bat = open(shell, "w")
        bat.write(str.join(" ", args))
        bat.close()
        system(shell)
        remove(shell)
        return MinecraftLaunchResponse(LaunchState.Success, args)