from json import loads
from os.path import exists, abspath, join
from os import makedirs, listdir
from modules.models.launch.game_core import GameCore
from modules.parser.game_core_parser import GameCoreParser


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
