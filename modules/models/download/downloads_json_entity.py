from modules.models.launch.file_json_entity import FileJsonEntity


class DownloadsJsonEntity():
    def __init__(self):
        self.artifact: FileJsonEntity
        self.classifiers: dict[str, FileJsonEntity]