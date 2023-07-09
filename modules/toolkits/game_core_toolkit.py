from modules.models.launch.game_core import GameCore


class GameCoreToolkit():
    def __init__(self, path: str = ".minecraft"):
        self.root = path

    def get_game_core(id: str) -> GameCore:
        pass # 咕咕ing，先放个pass占位
    
    def get_geme_cores() -> list[GameCore]:
        pass # 同上