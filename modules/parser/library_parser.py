from modules.models.download.downloads_json_entity import DownloadsJsonEntity
from modules.models.download.library_resource import LibraryResource
from modules.models.launch.file_json_entity import FileJsonEntity
from modules.models.launch.library_json_entity import LibraryJsonEntity
from modules.toolkits.environment_toolkit import EnvironmentToolkit


class LibraryParser():
    def __init__(self, entities: list[LibraryJsonEntity], root: str) -> None:
        self.entities = entities
        self.root = root

    def get_libraries(self) -> list[LibraryResource]:
        for library_json_entity in self.entities:
            obj: LibraryResource = LibraryResource()
            a = library_json_entity.downloads.artifact
            obj.check_sum = a.sha1 if a.sha1 != None else ""
            downloads: DownloadsJsonEntity = library_json_entity.downloads
            num: int
            if (downloads == None):
                num = 1
            else:
                artifact: FileJsonEntity = downloads.artifact
                if (artifact == None):
                    num = 1
                else:
                    _ = artifact.size
                    num = 0                
            obj.size = a.size if num == 1 else 0
            obj.url = (a.url if a.url != None else "") + library_json_entity.url
            obj.name = library_json_entity.name
            obj.root = self.root
            obj.is_enable = True
            library_resource: LibraryResource = obj
            if(library_json_entity.rules != None):
                library_resource.is_enable = self.__get_ability(library_json_entity, EnvironmentToolkit.get_platform_name())
            if(library_json_entity.natives != None):
                library_resource.is_natives = True
                if(not EnvironmentToolkit.get_platform_name() in library_json_entity.natives):
                    library_resource.is_enable = False
                if(library_resource.is_enable):
                    library_resource.name = f"{library_resource.name}:{self.__get_native_name(library_json_entity)}"
                    file: FileJsonEntity = library_json_entity.downloads.classifiers[library_json_entity.natives[EnvironmentToolkit.get_platform_name()].replace("${arch}", EnvironmentToolkit.arch)]
                    library_resource.check_sum = file.sha1
                    library_resource.size = file.size
                    library_resource.url = file.url
            yield library_resource

    def __get_native_name(self, library_json_entity: LibraryJsonEntity) -> str:
        return library_json_entity.natives[EnvironmentToolkit.get_platform_name()].replace("${arch}", EnvironmentToolkit.arch)
    
    def __get_ability(self, library_json_entity: LibraryJsonEntity, platform: str) -> bool:
        linux: bool
        osx: bool
        windows = linux = osx = False
        for item in library_json_entity.rules:
            if(item.action == "allow"):
                if(item.system == None):
                    windows = linux = osx = True
                    continue
                for enumerate2 in item.system.values():
                    match enumerate2:
                        case "windows":
                            windows = True
                        case "linux":
                            linux = True
                        case "osx":
                            osx = True
            else:
                if(not item.action == "disallow"):
                    continue
                if(item.system == None):
                    windows = linux = osx =False
                for enumerate2 in item.system.values():
                    match enumerate2:
                        case "windows":
                            windows = True
                        case "linux":
                            linux = True
                        case "osx":
                            osx = True
        match platform:
            case "windows":
                return windows
            case "linux":
                return linux
            case "osx":
                return osx
            case _:
                return False