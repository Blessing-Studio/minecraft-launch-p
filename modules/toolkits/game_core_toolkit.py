from json import loads
from os.path import exists
from os import makedirs, listdir
from modules.models.launch.game_core import GameCore
from modules.models.launch.game_core_json_entity import GameCoreJsonEntity
from modules.parser.game_core_parser import GameCoreParser


class GameCoreToolkit():
    def __init__(self, path: str = ".minecraft"):
        self.root = path
        self.error_game_cores: list[(str, Exception)]

    def get_game_core(self, id: str) -> GameCore:
        core: GameCore = GameCore()
        for core in self.get_geme_cores():
            if core.id == id:
                return core
        return None
    
    def get_geme_cores(self) -> list[GameCore]:
        entities: list[GameCoreJsonEntity] = []
        versions_folder: str = f"{self.root}\\versions"
        if (not exists(versions_folder)):
            makedirs(versions_folder)
            return []
        
        directories: list[str] = listdir(versions_folder)
        for item in directories:
            files2: list[str] = listdir(f"{versions_folder}\\{item}")
            for files in files2:
                if(files == f"{item}.json"):
                    entity: GameCoreJsonEntity = GameCoreJsonEntity()
                    try:
                        json_files = open(files)
                        entity = loads(json_files.read())
                        json_files.close()
                        entities.append(entity)
                    except:
                        ...
        parser: GameCoreParser = GameCoreParser(self.root, entities)
        game_cores: list[GameCore] = parser.get_game_cores
        self.error_game_cores = parser.error_game_cores
        return game_cores
