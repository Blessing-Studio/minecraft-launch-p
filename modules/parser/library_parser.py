from modules.models.download.library_resource import LibraryResource
from modules.utils.environment_util import EnvironmentUtil
from os.path import abspath


class LibraryParser():
    def __init__(self, entities: list[dict], root: str) -> None:
        self.entities = entities
        self.root = abspath(root)
        

    def get_libraries(self) -> list[LibraryResource]:
        for library_json_entity in self.entities:
            if ('artifact' in library_json_entity['downloads']):
                obj: LibraryResource = LibraryResource()
                a = library_json_entity['downloads']['artifact']
                obj.check_sum = a['sha1'] if a['sha1'] != None else ""
                downloads: dict = library_json_entity['downloads']
                num: int
                if (downloads == None):
                    num = 1
                else:
                    artifact: dict = downloads['artifact']
                    if (artifact == None):
                        num = 1
                    else:
                        _ = artifact['size']
                        num = 0                
                obj.size = a['size'] if num == 1 else 0
                obj.url = (a['url'] if 'url' in a else "") + (library_json_entity['url'] if 'url' in library_json_entity else "")
                obj.name = library_json_entity['name']
                obj.root = self.root
                obj.is_enable = True
                library_resource: LibraryResource = obj
                if('rules' in library_json_entity):
                    library_resource.is_enable = self.__get_ability(library_json_entity, EnvironmentUtil.get_platform_name())
                if('natives' in library_json_entity):
                    library_resource.is_natives = True
                    if(not EnvironmentUtil.get_platform_name() in library_json_entity['natives']):
                        library_resource.is_enable = False
                    if(library_resource.is_enable):
                        library_resource.name = f"{library_resource.name}:{self.__get_native_name(library_json_entity)}"
                        file: dict = library_json_entity['downloads']['classifiers'][library_json_entity['natives'][EnvironmentUtil.get_platform_name()].replace("${arch}", EnvironmentUtil.arch)]
                        library_resource.check_sum = file['sha1']
                        library_resource.size = file['size']
                        library_resource.url = file['url']
                yield library_resource
            else:
                return []

    def __get_native_name(self, library_json_entity: dict) -> str:
        return library_json_entity['natives'][EnvironmentUtil.get_platform_name()].replace("${arch}", EnvironmentUtil.arch)
    
    def __get_ability(self, library_json_entity: dict, platform: str) -> bool:
        linux: bool
        osx: bool
        windows = linux = osx = False
        for item in library_json_entity['rules']:
            if(item['action'] == "allow"):
                if(not 'system' in item):
                    windows = linux = osx = True
                    continue
                for enumerate2 in item['system'].values():
                    match enumerate2:
                        case "windows":
                            windows = True
                        case "linux":
                            linux = True
                        case "osx":
                            osx = True
            else:
                if(not item['action'] == "disallow"):
                    continue
                if(not 'system' in item):
                    windows = linux = osx =False
                
                if ('system' in item):
                    for enumerate2 in item['system'].values():
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