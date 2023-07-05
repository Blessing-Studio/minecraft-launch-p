from os.path import exists
from json import loads
import zipfile


class JavaMinecraftArgumentsBuilder():
    def __init__(self, mcDir: str, version: str, javawPath: str, maxMem: str, userName: str, width: str, height: str):
        self.McDir = mcDir
        self.Version = version
        self.JavawPath = javawPath
        self.MaxMem = maxMem
        self.UserName = userName
        self.Width = width
        self.Height = height

    def unpress(self, filename: str, path: str):
        Zip = zipfile.ZipFile(filename)
        for z in Zip.namelist():
            Zip.extract(z, path)
        Zip.close()

    def isMyversion(self, version: str, mcdir: str):
        if (exists(f"{mcdir}\\versions\\{version}\\{version}.json")):
            return True
        else:
            return False

    def Launch(self) -> str:
        commandLine = str("")
        JVM = str("")
        classPath = str("")
        mcArgs = str("")

        if ((not self.JavawPath == "")
                and (not self.Version == "")
                and (not self.MaxMem == "")
                and (not self.UserName == "")
                and (not self.McDir == "")):
            if (self.isMyversion(self.Version, self.McDir)):
                json = open(
                    f"{self.McDir}\\versions\\{self.Version}\\{self.Version}.json", "r")
                dic = loads(json.read())
                json.close()
                for lib in dic["libraries"]:
                    if "classifiers" in lib['downloads']:
                        for native in lib['downloads']:
                            if native == "artifact":
                                path = f"{self.McDir}\\versions\\{self.Version}\\natives"
                                filePath = f"{self.McDir}\\libraries\\{lib['downloads'][native]['path']}"
                                try:
                                    self.unpress(filePath, path)
                                except:
                                    pass
                            elif native == 'classifiers':
                                for n in lib['downloads'][native].values():
                                    path = f"{self.McDir}\\versions\\{self.Version}\\natives"
                                    filePath = f'{self.McDir}\\libraries\\{n["path"]}'
                                    try:
                                        self.unpress(filePath, path)
                                    except:
                                        pass
                JVM = '"' + self.JavawPath + '" -XX:+UseG1GC -XX:-UseAdaptiveSizePolicy' +\
                    ' -XX:-OmitStackTraceInFastThrow -Dfml.ignoreInvalidMinecraftCertificates=True ' +\
                    '-Dfml.ignorePatchDiscrepancies=True -Dlog4j2.formatMsgNoLookups=true ' +\
                    '-XX:HeapDumpPath=MojangTricksIntelDriversForPerformance_javaw.exe_minecraft.exe.heapdump ' +\
                    '-Dos.name="Windows 10" -Dos.version=10.0 -Djava.library.path="' +\
                    self.McDir + "\\versions\\" + self.Version + "\\" + "natives" +\
                    '" -Dminecraft.launcher.brand=launcher ' +\
                    '-Dminecraft.launcher.version=1.0.0 -cp'
                classPath += '"'
                for lib in dic["libraries"]:
                    if not 'classifiers' in lib["downloads"]:
                        normal = f'{self.McDir}\\libraries\\{lib["downloads"]["artifact"]["path"]}'
                        classPath += normal + ";"
                classPath = f'{classPath}{self.McDir}\\versions\\{self.Version}\\{self.Version}.jar"'
                JVM = f"{JVM} {classPath} -Xmx{self.MaxMem} -Xmn256m -Dlog4j.formatMsgNoLookups=true"

                mcArgs += dic["mainClass"] + " "
                if "minecraftArguments" in dic:
                    mcArgs += dic["minecraftArguments"]
                    mcArgs = mcArgs.replace(
                        "${auth_player_name}", self.UserName)  # 玩家名称
                    mcArgs = mcArgs.replace(
                        "${version_name}", self.Version)  # 版本名称
                    mcArgs = mcArgs.replace(
                        "${game_directory}", self.McDir)  # mc路径
                    mcArgs = mcArgs.replace(
                        "${assets_root}", self.McDir + "\\assets")  # 资源文件路径
                    mcArgs = mcArgs.replace(
                        "${assets_index_name}", dic["assetIndex"]["id"])  # 资源索引文件名称
                    mcArgs = mcArgs.replace(
                        "${auth_uuid}", "{}")  # 由于没有写微软登录,所以uuid为空的
                    mcArgs = mcArgs.replace(
                        "${auth_access_token}", "{}")  # 同上
                    mcArgs = mcArgs.replace("${clientid}", self.Version)  # 客户端id
                    mcArgs = mcArgs.replace("${auth_xuid}", "{}")  # 离线登录,不填
                    mcArgs = mcArgs.replace(
                        "${user_type}", "Legacy")  # 用户类型,离线模式是Legacy
                    mcArgs = mcArgs.replace(
                        "${version_type}", dic["type"])  # 版本类型
                    mcArgs = mcArgs.replace("${user_properties}", "{}")
                    mcArgs += f"--width {self.Width}"
                    mcArgs += f" --height {self.Height}"
                else:
                    for arg in dic["arguments"]["game"]:
                        if isinstance(arg, str):
                            mcArgs += arg + " "
                        elif isinstance(arg, dict):
                            if isinstance(arg["value"], list):
                                for a in arg["value"]:
                                    mcArgs += a + " "
                            elif isinstance(arg["value"], str):
                                mcArgs += arg["value"] + " "

                    mcArgs = mcArgs.replace(
                        "${auth_player_name}", self.UserName)  # 玩家名称
                    mcArgs = mcArgs.replace(
                        "${version_name}", self.Version)  # 版本名称
                    mcArgs = mcArgs.replace(
                        "${game_directory}", self.McDir)  # mc路径
                    mcArgs = mcArgs.replace(
                        "${assets_root}", self.McDir + "\\assets")  # 资源文件路径
                    mcArgs = mcArgs.replace(
                        "${assets_index_name}", dic["assetIndex"]["id"])  # 资源索引文件名称
                    mcArgs = mcArgs.replace(
                        "${auth_uuid}", "{}")  # 由于没有写微软登录,所以uuid为空的
                    mcArgs = mcArgs.replace(
                        "${auth_access_token}", "{}")  # 同上
                    mcArgs = mcArgs.replace("${clientid}", self.Version)  # 客户端id
                    mcArgs = mcArgs.replace("${auth_xuid}", "{}")  # 离线登录,不填
                    mcArgs = mcArgs.replace(
                        "${user_type}", "Legacy")  # 用户类型,离线模式是Legacy
                    mcArgs = mcArgs.replace(
                        "${version_type}", dic["type"])  # 版本类型
                    mcArgs = mcArgs.replace(
                        "${resolution_width}", self.Width)  # 窗口宽度
                    mcArgs = mcArgs.replace(
                        "${resolution_height}", self.Height)  # 窗口高度
                    mcArgs = mcArgs.replace("-demo ", "")  # 去掉-demo参数，退出试玩版

                commandLine = JVM + " " + mcArgs
                return commandLine
