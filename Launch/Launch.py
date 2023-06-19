from os.path import exists
from json import loads
from os import remove, system
import zipfile



def unpress(filename: str, path: str):
    Zip = zipfile.ZipFile(filename)
    for z in Zip.namelist():
        Zip.extract(z, path)
    Zip.close()

def isMyversion(version: str, mcdir: str):
    if(exists(f"{mcdir}\\versions\\{version}\\{version}.json")):
        return True
    else:
        return False

def Launch(mcdir: str, version: str, javaw_path: str, MaxMem: str, username: str, width: str, height: str):
    commandLine = str("")
    JVM = str("")
    classpath = str("")
    mc_args = str("")

    if((not javaw_path == "")\
        and (not version == "")\
        and (not MaxMem == "")\
        and (not username == "")\
        and (not mcdir == "")):
        if(isMyversion(version, mcdir)):
            version_json = open(f"{mcdir}\\versions\\{version}\\{version}.json", "r")
            dic = loads(version_json.read())
            version_json.close()
            for lib in dic["libraries"]:
                if "classifiers" in lib['downloads']:
                    for native in lib['downloads']:
                        if native == "artifact":
                            dirct_path = f"{mcdir}\\versions\\{version}\\natives"
                            filepath = f"{mcdir}\\libraries\\{lib['downloads'][native]['path']}"
                            try:
                                unpress(filepath, dirct_path)
                            except:
                                pass
                        elif native == 'classifiers':
                            for n in lib['downloads'][native].values():
                                dirct_path = f"{mcdir}\\versions\\{version}\\natives"
                                filepath = f'{mcdir}\\libraries\\{n["path"]}'
                                try:
                                    unpress(filepath, dirct_path)
                                except:
                                    pass
            JVM = '"' + javaw_path + '" -XX:+UseG1GC -XX:-UseAdaptiveSizePolicy' +\
            ' -XX:-OmitStackTraceInFastThrow -Dfml.ignoreInvalidMinecraftCertificates=True '+\
            '-Dfml.ignorePatchDiscrepancies=True -Dlog4j2.formatMsgNoLookups=true '+\
            '-XX:HeapDumpPath=MojangTricksIntelDriversForPerformance_javaw.exe_minecraft.exe.heapdump '+\
            '-Dos.name="Windows 10" -Dos.version=10.0 -Djava.library.path="'+\
            mcdir + "\\versions\\" + version + "\\" + "natives" +\
             '" -Dminecraft.launcher.brand=launcher '+\
            '-Dminecraft.launcher.version=1.0.0 -cp'
            classpath += '"'
            for lib in dic["libraries"]:
                if not 'classifiers' in lib["downloads"]:
                    normal = f'{mcdir}\\libraries\\{lib["downloads"]["artifact"]["path"]}'
                    classpath += normal + ";"
            classpath = f'{classpath}{mcdir}\\versions\\{version}\\{version}.jar"'
            JVM = f"{JVM} {classpath} -Xmx{MaxMem} -Xmn256m -Dlog4j.formatMsgNoLookups=true"

            mc_args += dic["mainClass"] + " "
            if "minecraftArguments" in dic:
                mc_args += dic["minecraftArguments"] 
                mc_args = mc_args.replace("${auth_player_name}", username)# 玩家名称
                mc_args = mc_args.replace("${version_name}", version)# 版本名称
                mc_args = mc_args.replace("${game_directory}", mcdir)# mc路径
                mc_args = mc_args.replace("${assets_root}", mcdir + "\\assets")# 资源文件路径
                mc_args = mc_args.replace("${assets_index_name}",dic["assetIndex"]["id"])# 资源索引文件名称
                mc_args = mc_args.replace("${auth_uuid}", "{}")# 由于没有写微软登录,所以uuid为空的
                mc_args = mc_args.replace("${auth_access_token}", "{}")# 同上
                mc_args = mc_args.replace("${clientid}", version)# 客户端id
                mc_args = mc_args.replace("${auth_xuid}", "{}")# 离线登录,不填
                mc_args = mc_args.replace("${user_type}", "Legacy")# 用户类型,离线模式是Legacy
                mc_args = mc_args.replace("${version_type}", dic["type"])# 版本类型
                mc_args = mc_args.replace("${user_properties}", "{}")
                mc_args += f"--width {width}"
                mc_args += f" --height {height}"
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
            
                mc_args = mc_args.replace("${auth_player_name}", username)# 玩家名称
                mc_args = mc_args.replace("${version_name}", version)# 版本名称
                mc_args = mc_args.replace("${game_directory}", mcdir)# mc路径
                mc_args = mc_args.replace("${assets_root}", mcdir + "\\assets")# 资源文件路径
                mc_args = mc_args.replace("${assets_index_name}",dic["assetIndex"]["id"])# 资源索引文件名称
                mc_args = mc_args.replace("${auth_uuid}", "{}")# 由于没有写微软登录,所以uuid为空的
                mc_args = mc_args.replace("${auth_access_token}", "{}")# 同上
                mc_args = mc_args.replace("${clientid}", version)# 客户端id
                mc_args = mc_args.replace("${auth_xuid}", "{}")# 离线登录,不填
                mc_args = mc_args.replace("${user_type}", "Legacy")# 用户类型,离线模式是Legacy
                mc_args = mc_args.replace("${version_type}", dic["type"])# 版本类型
                mc_args = mc_args.replace("${resolution_width}", width)# 窗口宽度
                mc_args = mc_args.replace("${resolution_height}", height)# 窗口高度
                mc_args = mc_args.replace("-demo ", "")# 去掉-demo参数，退出试玩版
            
            commandLine = JVM + " " + mc_args
            bat = open("run.bat", "w")
            bat.write(commandLine)
            bat.close()
            system("run.bat")
            remove("run.bat")