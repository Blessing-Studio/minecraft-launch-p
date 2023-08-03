class GameWindowConfig():
    def __init__(self, width: int = 854, height: int = 480, is_full_screen: bool = False) -> None:
        self.width: int = width
        self.height: int = height
        self.is_full_screen: bool = is_full_screen