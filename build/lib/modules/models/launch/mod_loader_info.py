from modules.enum.mod_loader_type import ModLoaderType


class ModLoaderInfo():
    def __init__(self, mod_loader_type: ModLoaderType, version: str):
        self.mod_loader_type: ModLoaderType = mod_loader_type
        self.version: str = version