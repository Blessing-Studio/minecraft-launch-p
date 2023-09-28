import os
import platform
from typing import Iterable
from os.path import exists, basename, join
from minecraft_launch.modules.utils.extend_util import ExtendUtil
from minecraft_launch.modules.models.launch.game_core import GameCore
from minecraft_launch.modules.models.launch.launch_config import LaunchConfig
from minecraft_launch.modules.utils.environment_util import EnvironmentUtil


class JavaMinecraftArgumentsBuilder():
    default_gc_arguments: list[str] = ["-XX:+UseG1GC", "-XX:+UnlockExperimentalVMOptions", "-XX:G1NewSizePercent=20", "-XX:G1ReservePercent=20", "-XX:MaxGCPauseMillis=50", "-XX:G1HeapRegionSize=16m", "-XX:-UseAdaptiveSizePolicy"]
    default_advanced_arguments: list[str] = ["-XX:-OmitStackTraceInFastThrow", "-XX:-DontCompileHugeMethods", "-Dfile.encoding=GB18030", "-Dfml.ignoreInvalidMinecraftCertificates=true", "-Dfml.ignorePatchDiscrepancies=true", "-Djava.rmi.server.useCodebaseOnly=true", "-Dcom.sun.jndi.rmi.object.trustURLCodebase=false", "-Dcom.sun.jndi.cosnaming.object.trustURLCodebase=false"]

    def __init__(self, game_core: GameCore, launch_config: LaunchConfig) -> None:
        self.game_core: GameCore = game_core
        self.launch_config: LaunchConfig = launch_config
            
    def build(self) -> Iterable[str]:
        yield f'"{self.launch_config.jvm_config.java_path}"'

        for front_arguments in self.get_front_arguments():
            yield front_arguments

        yield self.game_core.main_class

        for behind_arguments in self.get_behind_arguments():
            yield behind_arguments

    def get_behind_arguments(self) -> Iterable[str]:
        key_value_pairs: dict[str, str] = {
            "${auth_player_name}": self.launch_config.account.name,
            "${version_name}": self.game_core.id,
            "${assets_root}": join(self.game_core.root, "assets"),
            "${assets_index_name}": basename(self.game_core.assets_index_file.file_info).replace(".json", ""),
            "${auth_uuid}": self.launch_config.account.uuid.hex,
            "${auth_access_token}": self.launch_config.account.access_token,
            "${user_type}": "Mojang" ,
            "${version_type}":  self.game_core.type,
            "${user_properties}": "{}",
            "${game_assets}": join(self.game_core.root, "assets"),
            "${auth_session}": self.launch_config.account.access_token,
			"${game_directory}": join(self.game_core.root, "versions", self.game_core.id) if self.launch_config.is_enable_independency_core else self.game_core.root
        }

        List: list[str] = self.game_core.behind_arguments

        if(self.launch_config.game_window_config != None):
            List.append(f"--width {self.launch_config.game_window_config.width}")
            List.append(f"--height {self.launch_config.game_window_config.height}")
            if(self.launch_config.game_window_config.is_full_screen):
                List.append("--fullscreen")

        if(self.launch_config.server_config != None):
            if(self.launch_config.server_config.ip != None & self.launch_config.server_config.ip != "")&(self.launch_config.server_config.port != 0):
                List.append(f"--server {self.launch_config.server_config.ip}")
                List.append(f"--port {self.launch_config.server_config.port}")

        for item in List:
            yield ExtendUtil.replace(item, key_value_pairs)
        
    def get_front_arguments(self) -> Iterable[str]:
        key_value_pairs: dict[str, str] = {
            "${launcher_name}": "minecraft-launch-p",
            "${launcher_version}": "3",
            "${classpath_separator}": ";",
            "${classpath}": self.__get_classpath(),
            "${client}": self.game_core.client_file.file_info,
            "${min_memory}": str(self.launch_config.jvm_config.min_memory),
            "${max_memory}": str(self.launch_config.jvm_config.max_memory),
            "${library_directory}": join(self.game_core.root, "libraries"),
            "${version_name}": self.game_core.id if self.game_core.inherits_from in [None, ""] else self.game_core.inherits_from,           
            "${natives_directory}": self.launch_config.natives_folder if self.launch_config.natives_folder != None and exists(self.launch_config.natives_folder) else join(self.game_core.root, "versions", self.game_core.id, "natives"),
            }
        
        if(not exists(key_value_pairs["${natives_directory}"])):
            os.makedirs(key_value_pairs["${natives_directory}"].strip('"'))
        
        args: list[str] = [ "-Xmn${min_memory}m", "-Xmx${max_memory}m", "-Dminecraft.client.jar=${client}"]

        for item in self.__get_environment_jvm_arguments():
            args.append(item)

        if(self.launch_config.jvm_config.gc_arguments == None):
            for x in self.default_gc_arguments:
                args.append(x)
        else:
            for x in self.launch_config.jvm_config.gc_arguments:
                args.append(x)
        
        if(self.launch_config.jvm_config.advanced_arguments == None):
            for x in self.default_advanced_arguments:
                args.append(x)
        else:
            for x in self.launch_config.jvm_config.advanced_arguments:
                args.append(x)

        args.append("-Dlog4j2.formatMsgNoLookups=true")
        for item3 in self.game_core.front_arguments:
            args.append(item3)

        for item2 in args:
            yield ExtendUtil.replace(item2, key_value_pairs)


    def __get_classpath(self) -> str:
        loads = []
        for x in self.game_core.library_resources:
            if(x.is_enable)&(not x.is_natives):
                loads.append(x)
        loads.append(self.game_core.client_file)
        __loads = [x.to_file_info() for x in loads]
        return str.join(";", __loads)
    
    @staticmethod
    def __get_environment_jvm_arguments() -> Iterable[str]:
        platform_name: str = EnvironmentUtil.get_platform_name()
        if(not platform_name == "windows"):
            if(platform_name == "osx"):
                yield  "-XstartOnFirstThread"
        else:
            yield "-XX:HeapDumpPath=MojangTricksIntelDriversForPerformance_javaw.exe_minecraft.exe.heapdump"
            if("10.0" in platform.version()):
                yield "-Dos.name=\"Windows 10\""
                yield "-Dos.version=10.0"
        if(EnvironmentUtil.arch == "32"):
            yield "-Xss1M"
