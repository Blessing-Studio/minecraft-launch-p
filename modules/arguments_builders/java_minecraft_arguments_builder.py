from os.path import exists, basename
import platform
from modules.models.download.library_resource import LibraryResource
from modules.models.launch.game_core import GameCore
from modules.models.launch.launch_config import LaunchConfig
import os
from modules.utils.environment_util import EnvironmentUtil
from modules.utils.extend_util import ExtendUtil


class JavaMinecraftArgumentsBuilder():
    default_gc_arguments: list[str] = ["-XX:+UseG1GC", "-XX:+UnlockExperimentalVMOptions", "-XX:G1NewSizePercent=20", "-XX:G1ReservePercent=20", "-XX:MaxGCPauseMillis=50", "-XX:G1HeapRegionSize=16m", "-XX:-UseAdaptiveSizePolicy"]
    default_advanced_arguments: list[str] = ["-XX:-OmitStackTraceInFastThrow", "-XX:-DontCompileHugeMethods", "-Dfile.encoding=GB18030", "-Dfml.ignoreInvalidMinecraftCertificates=true", "-Dfml.ignorePatchDiscrepancies=true", "-Djava.rmi.server.useCodebaseOnly=true", "-Dcom.sun.jndi.rmi.object.trustURLCodebase=false", "-Dcom.sun.jndi.cosnaming.object.trustURLCodebase=false"]

    def __init__(self, game_core: GameCore, launch_config: LaunchConfig) -> None:
        self.game_core = game_core
        self.launch_config = launch_config

        '''self.path = game_core.root
        self.version = game_core.id
        self.javaw_path = launch_config.jvm_config.java_path
        self.max_memory = f'{launch_config.jvm_config.max_memory}m' 
        self.user_name = launch_config.account.name
        self.width = launch_config.game_window_config.width
        self.height = launch_config.game_window_config.height'''

    '''def unpress(self, name: str, path: str) -> None:
        zip = zipfile.ZipFile(name)
        for z in zip.namelist():
            zip.extract(z, path)
        zip.close()

    def is_my_version(self, version: str, path: str) -> bool:
        if (exists(f"{path}\\versions\\{version}\\{version}.json")):
            return True
        else:
            return False

    def build(self) -> str:
        command_line: str
        jvm: str
        class_path: str = ""
        mc_args: str = ""

        if ((not self.javaw_path == "")
                and (not self.version == "")
                and (not self.max_memory == "")
                and (not self.user_name == "")
                and (not self.path == "")):
            if (self.is_my_version(self.version, self.path)):
                json = open(
                    f"{self.path}\\versions\\{self.version}\\{self.version}.json", "r")
                dic: dict = loads(json.read())
                json.close()
                for lib in dic["libraries"]:
                    if "classifiers" in lib['downloads']:
                        for native in lib['downloads']:
                            if native == "artifact":
                                path = f"{self.path}\\versions\\{self.version}\\natives"
                                filePath = f"{self.path}\\libraries\\{lib['downloads'][native]['path']}"
                                try:
                                    self.unpress(filePath, path)
                                except:
                                    pass
                            elif native == 'classifiers':
                                for n in lib['downloads'][native].values():
                                    path = f"{self.path}\\versions\\{self.version}\\natives"
                                    filePath = f'{self.path}\\libraries\\{n["path"]}'
                                    try:
                                        self.unpress(filePath, path)
                                    except:
                                        ...
                jvm = '"' + self.javaw_path + '" -XX:+UseG1GC -XX:-UseAdaptiveSizePolicy' +\
                    ' -XX:-OmitStackTraceInFastThrow -Dfml.ignoreInvalidMinecraftCertificates=True ' +\
                    '-Dfml.ignorePatchDiscrepancies=True -Dlog4j2.formatMsgNoLookups=true ' +\
                    '-XX:HeapDumpPath=MojangTricksIntelDriversForPerformance_javaw.exe_minecraft.exe.heapdump ' +\
                    '-Dos.name="Windows 10" -Dos.version=10.0 -Djava.library.path="' +\
                    self.path + "\\versions\\" + self.version + "\\" + "natives" +\
                    '" -Dminecraft.launcher.brand=launcher ' +\
                    '-Dminecraft.launcher.version=1.0.0 -cp'
                class_path += '"'
                for lib in dic["libraries"]:
                    if not 'classifiers' in lib["downloads"]:
                        normal = f'{self.path}\\libraries\\{lib["downloads"]["artifact"]["path"]}'
                        class_path += normal + ";"
                class_path = f'{class_path}{self.path}\\versions\\{self.version}\\{self.version}.jar"'
                jvm = f"{jvm} {class_path} -Xmx{self.max_memory} -Xmn256m -Dlog4j.formatMsgNoLookups=true"

                mc_args += dic["mainClass"] + " "
                if "minecraftArguments" in dic:
                    mc_args += dic["minecraftArguments"]
                    mc_args = mc_args.replace(
                        "${auth_player_name}", self.user_name)  # 玩家名称
                    mc_args = mc_args.replace(
                        "${version_name}", self.version)  # 版本名称
                    mc_args = mc_args.replace(
                        "${game_directory}", self.path)  # mc路径
                    mc_args = mc_args.replace(
                        "${assets_root}", f'{self.path}\\assets')  # 资源文件路径
                    mc_args = mc_args.replace(
                        "${assets_index_name}", dic["assetIndex"]["id"])  # 资源索引文件名称
                    mc_args = mc_args.replace(
                        "${auth_uuid}", "{}")  # 由于没有写微软登录,所以uuid为空的
                    mc_args = mc_args.replace(
                        "${auth_access_token}", "{}")  # 同上
                    mc_args = mc_args.replace(
                        "${clientid}", self.version)  # 客户端id
                    mc_args = mc_args.replace("${auth_xuid}", "{}")  # 离线登录,不填
                    mc_args = mc_args.replace(
                        "${user_type}", "Legacy")  # 用户类型,离线模式是Legacy
                    mc_args = mc_args.replace(
                        "${version_type}", dic["type"])  # 版本类型
                    mc_args = mc_args.replace("${user_properties}", "{}")
                    mc_args += f"--width {self.width}"
                    mc_args += f" --height {self.height}"
                else:
                    for arg in dic["arguments"]["game"]:
                        if isinstance(arg, str):
                            mc_args += arg + " "
                        elif isinstance(arg, dict):
                            if isinstance(arg["value"], list):
                                for a in arg["value"]:
                                    mc_args += a + " "
                            elif isinstance(arg["value"], str):
                                mc_args += arg["value"] + " "

                    mc_args = mc_args.replace(
                        "${auth_player_name}", self.user_name)  # 玩家名称
                    mc_args = mc_args.replace(
                        "${version_name}", self.version)  # 版本名称
                    mc_args = mc_args.replace(
                        "${game_directory}", self.path)  # mc路径
                    mc_args = mc_args.replace(
                        "${assets_root}", self.path + "\\assets")  # 资源文件路径
                    mc_args = mc_args.replace(
                        "${assets_index_name}", dic["assetIndex"]["id"])  # 资源索引文件名称
                    mc_args = mc_args.replace(
                        "${auth_uuid}", "{}")  # 由于没有写微软登录,所以uuid为空的
                    mc_args = mc_args.replace(
                        "${auth_access_token}", "{}")  # 同上
                    mc_args = mc_args.replace(
                        "${clientid}", self.version)  # 客户端id
                    mc_args = mc_args.replace("${auth_xuid}", "{}")  # 离线登录,不填
                    mc_args = mc_args.replace(
                        "${user_type}", "Legacy")  # 用户类型,离线模式是Legacy
                    mc_args = mc_args.replace(
                        "${version_type}", dic["type"])  # 版本类型
                    mc_args = mc_args.replace(
                        "${resolution_width}", str(self.width))  # 窗口宽度
                    mc_args = mc_args.replace(
                        "${resolution_height}", str(self.height))  # 窗口高度
                    mc_args = mc_args.replace("-demo ", "")  # 去掉-demo参数，退出试玩版

                command_line = jvm + " " + mc_args
                return command_line'''
            
    def build(self) -> list[str]:
        yield f'"{self.launch_config.jvm_config.java_path}"'

        for front_arguments in self.get_front_arguments():
            yield front_arguments

        yield self.game_core.main_class

        for behind_arguments in self.get_behind_arguments():
            yield behind_arguments

    def get_behind_arguments(self) -> list[str]:
        key_value_pairs: dict[str, str] = {
            "${auth_player_name}": self.launch_config.account.name,
            "${version_name}": self.game_core.id,
            "${assets_root}": f'{self.game_core.root}\\assets',
            "${assets_index_name}": basename(self.game_core.assets_index_file.file_info).replace(".json", ""),
            "${auth_uuid}": self.launch_config.account.uuid.hex,
            "${auth_access_token}": self.launch_config.account.access_token,
            "${user_type}": "Mojang" ,
            "${version_type}":  self.game_core.type,
            "${user_properties}": "{}",
            "${game_assets}": f"{self.game_core.root}\\assets",
            "${auth_session}": self.launch_config.account.access_token,
			"${game_directory}": f"{self.game_core.root}\\versions\\{self.game_core.id}" if self.launch_config.is_enable_independency_core else self.game_core.root
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
        
    def get_front_arguments(self) -> list[str]:
        key_value_pairs: dict[str, str] = {
            "${launcher_name}": "minecraft-launch-p",
            "${launcher_version}": "3",
            "${classpath_separator}": os.sep,
            "${classpath}": self.__get_classpath(),
            "${client}": self.game_core.client_file.file_info,
            "${min_memory}": str(self.launch_config.jvm_config.min_memory),
            "${max_memory}": str(self.launch_config.jvm_config.max_memory),
            "${library_directory}": f"{self.game_core.root}\\libraries",
            "${version_name}": self.game_core.id if self.game_core.inherits_from == None or self.game_core.inherits_from == "" else self.game_core.inherits_from,           
            "${natives_directory}": self.launch_config.natives_folder if self.launch_config.natives_folder != None and exists(self.launch_config.natives_folder) else f"{self.game_core.root}\\versions\\{self.game_core.id}\\natives",
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
    def __get_environment_jvm_arguments() -> list[str]:
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
