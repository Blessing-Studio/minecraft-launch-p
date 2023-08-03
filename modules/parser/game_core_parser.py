from genericpath import exists
from json import loads
from modules.enum.mod_loader_type import ModLoaderType
from modules.models.download.api_manager import APIManager
from modules.models.download.file_resource import FileResource
from modules.models.launch.game_core import GameCore
from modules.parser.library_parser import LibraryParser
from os.path import basename, abspath, join
from modules.models.launch.mod_loader_info import ModLoaderInfo


class GameCoreParser(): 
    def __init__(self, root: str, json_entities: list[dict]) -> None:
        self.root = abspath(root)
        self.json_entities = json_entities
        self.error_game_cores: list[(str, Exception)] = []

    def get_game_cores(self) -> list[GameCore]:
        cores: list[GameCore] = []
        for json_entity in self.json_entities:
            # try:
                game_core: GameCore = GameCore()
                game_core.id = json_entity['id']
                game_core.type = json_entity['type']
                game_core.root = self.root
                game_core.main_class = json_entity['mainClass']
                game_core.inherits_from = json_entity['inheritsFrom'] if "inheritsFrom" in json_entity else None
                game_core.java_version = json_entity['javaVersion']['majorVersion'] if 'javaVersion' in json_entity else None 
                game_core.library_resources = list(LibraryParser(json_entity['libraries'], self.root).get_libraries())

                if(not 'inheritsFrom' in json_entity)&('downloads' in json_entity):
                    game_core.client_file =  self.__get_client_file(json_entity)

                if(not 'inheritsFrom' in json_entity)&('logging' in json_entity):
                    if('client' in json_entity['logging']):
                        game_core.log_config_file = self.__get_log_config_file(json_entity)

                if(not 'inheritsFrom' in json_entity)&('assetIndex' in json_entity):
                    game_core.assets_index_file = self.__get_assets_index_file(json_entity)

                if('minecraftArguments' in json_entity):
                    game_core.behind_arguments = self.__handle_minecraft_arguments(json_entity['minecraftArguments'])

                if('arguments' in json_entity):
                    if('game' in json_entity['arguments']):
                        if(game_core.behind_arguments != None):
                            behind_arguments: list[str] = game_core.behind_arguments
                            behind_arguments += self.__handle_arguments_game(json_entity['arguments']) 
                        else:
                            behind_arguments: list[str] = self.__handle_arguments_game(json_entity['arguments'])

                        game_core.behind_arguments = behind_arguments

                if('arguments' in json_entity):
                    if('jvm' in json_entity['arguments']):
                        game_core.front_arguments = self.__handle_arguments_jvm(json_entity["arguments"])
                    else:
                        game_core.front_arguments = ["-Djava.library.path=${natives_directory}", "-Dminecraft.launcher.brand=${launcher_name}", "-Dminecraft.launcher.version=${launcher_version}", "-cp ${classpath}"]
                else:
                    game_core.front_arguments = ["-Djava.library.path=${natives_directory}", "-Dminecraft.launcher.brand=${launcher_name}", "-Dminecraft.launcher.version=${launcher_version}", "-cp ${classpath}"]
                
                cores.append(game_core)
            # except Exception as item:
              #  self.error_game_cores.append((json_entity.id, item))
        
        for item2 in cores:
            item2.source = self.__get_source(item2)
            item2.has_mod_loader = self.__get_has_mod_loader(item2)

            if(item2.has_mod_loader):
                item2.mod_loader_infos = self.__get_mod_loader_infos(item2)

            if(item2.inherits_from == None):
                yield item2
                continue
            game_core2: GameCore = GameCore()
            for item3 in cores:
                if(item3.id == item2.inherits_from):
                    game_core2 = item3
            
            if(game_core2 != None):
                yield self.__combine(item2, game_core2)

    def __get_client_file(self, entity: dict) -> FileResource:
        text: str = join(self.root, "versions", entity['id'], f"{entity['id']}.jar")
        return FileResource(
            check_sum = entity['downloads']["client"]['sha1'],
            size = entity['downloads']['client']['size'],
            url = entity['downloads']["client"]['url'].replace("https://launcher.mojang.com", APIManager.current.host) if APIManager.current != APIManager.mojang else entity["downloads"]["client"]["url"],
            root = self.root,
            file_info = text,
            name = basename(text)
        )

    def __get_log_config_file(self, entity: dict) -> FileResource:
        mid = entity['logging']['client']['file']['url']
        file_name: str = join(self.root, "versions", entity['id'], entity['logging']['client']['file']['id'] if entity['logging']['client']['file']['id'] != None else basename(mid))
        return FileResource(
            check_sum = entity['logging']['client']['file']['sha1'],
			size = entity['logging']['client']['file']['size'],
			url = entity['logging']['client']['file']['url'].replace("https://launcher.mojang.com", APIManager.current.host) if APIManager.current != APIManager.mojang else entity['logging']['client']['file']['url'],
			name = entity['logging']['client']['file']['id'],
			file_info = file_name,
			root = self.root
        )
    
    def __get_assets_index_file(self, entity: dict) -> FileResource:
        file_name: str = join(self.root, "assets", "indexes", f"{entity['assetIndex']['id']}.json")
        return FileResource(
            check_sum = entity['assetIndex']['sha1'],
			size = entity['assetIndex']['size'],
			url = (entity['assetIndex']['url'].replace("https://launchermeta.mojang.com", APIManager.current.host) if "https://launchermeta.mojang.com" in entity["assetIndex"]["url"] else entity["assetIndex"]["url"].replace("https://piston-meta.mojang.com", APIManager.current.host)) if APIManager.current != APIManager.mojang else entity['assetIndex']['url'],
			name = f"{entity['assetIndex']['id']}.json",
			file_info = file_name,
			root = self.root
        )
    
    def __get_source(self, core: GameCore) ->str:
        try:
            path: str = join(core.root, "versions", core.id, f"{core.id}.json")
            if(core.inherits_from != None):
                return core.inherits_from
            if(exists(path)):
                json = open(path)
                jobject = loads(json.read())
                json.close()
                if("patches" in jobject):
                    return jobject["patches"][0]["version"]
                if("clientVersion" in jobject):
                    return jobject["clientVersion"]
        except:
            ...
        return core.id
    
    def __get_has_mod_loader(self, core: GameCore) -> bool:
        for enumerator in core.behind_arguments:
            match enumerator:
                case "--tweakClass optifine.OptiFineTweaker":
                    return True
                case "--tweakClass net.minecraftforge.fml.common.launcher.FMLTweaker":
                    return True
                case "--fml.forgeGroup net.minecraftforge":
                    return True
        
        for front_arguments in core.front_arguments:
            if("-DFabricMcEmu= net.minecraft.client.main.Main" in front_arguments):
                return True
            
        match core.main_class:
            case "net.minecraft.client.main.Main":
                return False
            case "net.minecraft.launchwrapper.Launch":
                return False
            case "com.mojang.rubydung.RubyDung":		
                return False
            case _:
                return True
                
    def __get_mod_loader_infos(self, core: GameCore) -> list[ModLoaderInfo]:
        lib_find = [lib for lib in core.library_resources 
                    if (str(lib.name.lower).startswith("optifine:optifine")) or\
                    (str(lib.name.lower).startswith("net.minecraftforge:forge:")) or\
                    (str(lib.name.lower).startswith("net.minecraftforge:fmlloader:")) or\
                    (str(lib.name.lower).startswith("net.fabricmc:fabric-loader")) or\
                    (str(lib.name.lower).startswith("com.mumfrey:liteloader:")) or\
                    (str(lib.name.lower).startswith("org.quiltmc:quilt-loader"))
                    ]
        
        for lib in lib_find:
            lower_name = lib.name.lower()
            id = lib.name.split(':')[2]

            if (lower_name.startswith("optifine:optifine")):
                yield ModLoaderInfo(mod_loader_type = ModLoaderType.OptiFine, version = id[id.find('_') + 1])
            elif (lower_name.startswith("net.minecraftforge:forge:") or\
                lower_name.startswith("net.minecraftforge:fmlloader:")):
                yield  ModLoaderInfo(mod_loader_type = ModLoaderType.Forge, version = id.split('-')[1])
            elif (lower_name.startswith("net.fabricmc:fabric-loader")):
                yield ModLoaderInfo(mod_loader_type = ModLoaderType.Fabric, version = id)
            elif (lower_name.startswith("com.mumfrey:liteloader:")):
                yield ModLoaderInfo(mod_loader_type = ModLoaderType.LiteLoader, version = id) 
            elif(lower_name.startswith("org.quiltmc:quilt-loader")):
                yield ModLoaderInfo(mod_loader_type = ModLoaderType.Quilt, version = id)

    
    def __handle_minecraft_arguments(self, minecraft_arguments: str) -> list[str]:
        return minecraft_arguments.replace("  ", " ").split(' ')
    
    def __handle_arguments_game(self, entity: dict) -> list[str]:
        return [i for i in entity['game'] if type(i) == str]
    
    def __handle_arguments_jvm(self, entity: dict) -> list[str]:
        return [i for i in entity['jvm'] if type(i) == str]
    
    @staticmethod
    def __arguments_group(vs: list[str]) -> list[str]:
        cache: list[str] = []
        for item in vs:
            if(any(cache)):
                if (cache[0].startswith("-") & item.startswith("-")):
                    yield cache[0].strip(' ')
                    cache = [item]
            elif(vs[-1] == item)&(not any(cache)):
                yield item.strip(' ')
            else:
                cache.append(item)
            if(len(cache) == 2):
                yield str.join(" ", cache).strip(' ')
                cache = []

    def __combine(self, raw: GameCore, inherits_from: GameCore) -> GameCore:
        raw.assets_index_file = inherits_from.assets_index_file
        raw.client_file = inherits_from.client_file
        raw.log_config_file = inherits_from.log_config_file
        raw.java_version = inherits_from.java_version
        raw.type = inherits_from.type
        raw.library_resources = list(set(raw.library_resources).union(set(inherits_from.library_resources)))
        raw.behind_arguments = list(set(inherits_from.behind_arguments).union(set(raw.behind_arguments)))
        raw.front_arguments = list(set(raw.front_arguments).union(set(inherits_from.front_arguments)))
        return raw