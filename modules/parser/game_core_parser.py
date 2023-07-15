from modules.models.launch.game_core_json_entity import GameCoreJsonEntity
from modules.models.launch.game_core import GameCore
from library_parser import LibraryParser

class GameCoreParser(): 
    error_game_cores: list[str, Exception]
    def __init__(self, root: str, json_entities: list[GameCoreJsonEntity]):
        self.root = root
        self.json_entities = json_entities
    def get_game_cores(self) ->list[GameCore]:
		
        for json_entity in self.json_entities:
            try:
                game_core: GameCore = GameCore
                game_core.id = json_entity.id
                game_core.type = json_entity.type
                game_core.main_class = json_entity.main_class
                game_core.inherits_form = json_entity.inherits_form
                game_core.java_version = json_entity.java_version.major_version
                game_core.library_resources = list(LibraryParser(json_entity.libraries, self.root).get_libraries())
                game_core.root = self.root
            except:
                ...