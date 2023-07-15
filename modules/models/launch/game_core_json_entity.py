from modules.models.launch.java_version_json_entity import JavaVersionJsonEntity
from modules.models.launch.library_json_entity import LibraryJsonEntity

class GameCoreJsonEntity():
    id: str
    root: str
    type: str
    main_class: str
    inherits_form: str
    java_version = JavaVersionJsonEntity()
    java_version.major_version = 8
    libraries: list[LibraryJsonEntity]
