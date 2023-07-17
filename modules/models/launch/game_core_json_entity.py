from modules.models.launch.arguments_json_entity import ArgumentsJsonEntity
from modules.models.launch.asset_index_json_entity import AssetIndexJsonEntity
from modules.models.launch.file_json_entity import FileJsonEntity
from modules.models.launch.java_version_json_entity import JavaVersionJsonEntity
from modules.models.launch.library_json_entity import LibraryJsonEntity
from modules.models.launch.logging_json_entity import LoggingJsonEntity

class GameCoreJsonEntity():
    def __init__(self):
        self.arguments: ArgumentsJsonEntity
        self.id: str
        self.root: str
        self.type: str
        self.main_class: str
        self.inherits_form: str
        self.java_version = JavaVersionJsonEntity()
        self.java_version.major_version = 8
        self.libraries: list[LibraryJsonEntity]
        self.downloads: dict[str, FileJsonEntity]
        self.logging: LoggingJsonEntity
        self.assets_index: AssetIndexJsonEntity
        self.minecraft_arguments: str
