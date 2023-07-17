from modules.models.launch.file_json_entity import FileJsonEntity


class ClientJsonEntity():
    def __init__(self):
        self.argument: str
        self.file: FileJsonEntity
        self.type: str