from os.path import exists
from json import loads
from modules.models.launch.game_core import GameCore
from modules.models.launch.launch_config import LaunchConfig
import zipfile


class JavaMinecraftArgumentsBuilder():
    # new __init__
    def __init__(self, game_core: GameCore, launch_config: LaunchConfig) -> None:
        self.game_core = game_core
        self.launch_config = launch_config
        '''self.path = game_core.root
        self.version = game_core.id
        self.javawpath = launch_config.jvm_config[0] 
        self.max_memory = launch_config.jvm_config[1] 
        self.user_name = launch_config.account
        self.width = launch_config.game_window_config[0] 
        self.height = launch_config.game_window_config[1]'''

    # old __init__，暂时先不改     
    def __init__(self, path: str, version: str, javaw_path: str, max_memory: str, user_name: str, width: str, height: str):
        self.path = path
        self.version = version
        self.javaw_path = javaw_path
        self.max_memory = max_memory
        self.user_name = user_name
        self.width = width
        self.height = height

    def unpress(self, name: str, path: str) -> None:
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
        class_path: str
        mc_args: str

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
                        "${resolution_width}", self.width)  # 窗口宽度
                    mc_args = mc_args.replace(
                        "${resolution_height}", self.height)  # 窗口高度
                    mc_args = mc_args.replace("-demo ", "")  # 去掉-demo参数，退出试玩版

                command_line = jvm + " " + mc_args
                return command_line
