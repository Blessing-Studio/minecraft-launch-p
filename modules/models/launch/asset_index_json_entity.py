from modules.models.launch.file_json_entity import FileJsonEntity


class AssetIndexJsonEntity(FileJsonEntity):
    def __init__(self):
        self.total_size: int