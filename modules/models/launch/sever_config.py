class SeverConfig():
    def __init__(self, port: int = 0, ip: str|None = None):
        self.port: int = port
        self.ip: str|None = ip
