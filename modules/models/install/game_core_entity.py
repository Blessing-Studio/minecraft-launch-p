class GameCoreEntity():
    def __init__(self, json: dict):
        self.id: str = json["id"]
        self.type: str = json["type"]
        self.url: str = json["url"]
        self.time: str = json["time"]
        self.release_time: str = json["releaseTime"]