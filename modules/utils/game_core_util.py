from json import dumps, loads
from shutil import move, rmtree
from os.path import exists, abspath, join, isfile, isdir
from os import makedirs, listdir
import traceback
from modules.models.launch.game_core import GameCore
from modules.parser.game_core_parser import GameCoreParser
from modules.utils.extend_util import ExtendUtil


class GameCoreUtil():
    def __init__(self, path: str = ".minecraft"):
        self.root = abspath(path)
        self.error_game_cores: list[(str, Exception)]

    def get_game_core(self, id: str) -> GameCore:
        core: GameCore = GameCore()
        for core in self.get_geme_cores():
            if core.id == id:
                return core
        return None
    
    def get_geme_cores(self) -> list[GameCore]:
        entities: list[dict] = []
        versions_folder: str = join(self.root, "versions")
        if (not exists(versions_folder)):
            makedirs(versions_folder)
            return []
        
        directories: list[str] = listdir(versions_folder)
        for item in directories:
            files2: list[str] = listdir(join(versions_folder, item))
            for file in files2:
                if(file == f"{item}.json"):
                    entity: dict = {}
                    try:
                        json_file = open(join(self.root, "versions", item, file))
                        entity = loads(json_file.read())
                        json_file.close()
                        entities.append(entity)
                    except:
                       ...
        parser: GameCoreParser = GameCoreParser(self.root, entities)
        game_cores: list[GameCore] = parser.get_game_cores()
        self.error_game_cores = parser.error_game_cores
        return game_cores
    
    def __get_game_core_json_entity(self, id: str, inheritsfrom: str) -> dict:
        versions_folder: str = join(self.root, "versions")
        if(not exists(versions_folder)):
            makedirs(versions_folder)
            return None
        
        directories: list = [j for j in listdir(versions_folder) if isdir(join(versions_folder, j))]
        for i in directories:
            files: list = [j for j in listdir(i) if isfile(join(i, j))]
            for file in files:
                if(file == f"{i}.json"):
                    with open(file) as json:
                        entity: dict = loads(json.read())
                    if (entity["id"] == id):
                        entity["inheritsFrom"] = inheritsfrom
                        return entity
        return None
    
    def rename(self, oldid: str, newid: str) -> GameCore:
        version_path: str = join(self.root, "versions")
        game_json: str = join(version_path, oldid, f"{oldid}.json")
        game_jar: str = join(version_path, oldid, f"{oldid}.jar")
        game_folder: str = join(self.root, "versions", oldid)

        try:
            json = open(game_json)
            entity: dict = loads(json.read())
            json.close()
            entity["id"] = newid

            for i in self.get_geme_cores():
                if("inheritsFrom" in entity):
                    if(entity["inheritsFrom"] == oldid):
                        entity["inheritsFrom"] = newid
                        with open(join(i.root, "versions", i.id, f"{i.id}.json"), "w") as json:
                            json.write(dumps(self.__get_game_core_json_entity(i.id, i.inherits_from)))
                
            with open(game_json, "w") as json:
                json.write(dumps(entity))
            
            move(game_jar, join(self.root, "versions", oldid, f"{newid}.jar"))
            move(game_json, join(self.root, "versions", oldid , f"{newid}.json"))
            move(game_folder, join(self.root, "versions", newid))
            ExtendUtil.beautifyjson(join(self.root, "versions", newid , f"{newid}.json"))

        except Exception as ex:
            print(f"[minecraft-launch-p][GameCoreUtil/rename]: {str(ex)}\n{traceback.print_exc()}")
            raise

        return self.get_game_core(newid)

    def delete(self, id: str) -> None:
        directory: str = join(self.root, "versions", id)
        if(exists(directory)):
            rmtree(directory)
        
    