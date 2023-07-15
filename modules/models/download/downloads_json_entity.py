from modules.models.launch.file_json_entity import FileJsonEntity


class DownloadsJsonEntity():
    artifact: FileJsonEntity
    classifiers: dict[str, FileJsonEntity]