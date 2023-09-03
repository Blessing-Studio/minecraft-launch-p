from modules.models.install.game_core_entity import GameCoreEntity


class GameCoresEntity():
    def __init__(self, json: dict):
        self.latest: dict[str, str] = json["latest"]
        cores: list[dict] = json["versions"]
        self.cores: list[GameCoreEntity] = []
        for i in cores:
            core = GameCoreEntity(i)
            self.cores.append(core)