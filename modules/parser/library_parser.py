from minecraft_launch.modules.models.download.library_resource import LibraryResource
from minecraft_launch.modules.utils.environment_util import EnvironmentUtil
from os.path import abspath


class LibraryParser():
    def __init__(self, entities: list[dict], root: str) -> None:
        self.entities = entities
        self.root = abspath(root)
        

    def get_libraries(self) -> list[LibraryResource]:
        for library_json_entity in self.entities:
            obj: LibraryResource = LibraryResource()
            if("downloads" in library_json_entity):
                num = 0
                if ('artifact' in library_json_entity['downloads']):
                    a = library_json_entity['downloads']['artifact']
                    num = 0
                else:
                    a = None
                    num = 1
            else:
                a = None
            if a != None:
                obj.url = (a['url'] if 'url' in a else "") + (library_json_entity['url'] if 'url' in library_json_entity else "")
                obj.size = a['size'] if 'size' in a and num == 0 else 0                
                obj.check_sum = a['sha1'] if 'sha1' in a else ""
            else:
                obj.check_sum = ""
                num = 0

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
            else:
                library_resource.is_natives = False
                
            yield library_resource

    def __get_native_name(self, library_json_entity: dict) -> str:
        return library_json_entity['natives'][EnvironmentUtil.get_platform_name()].replace("${arch}", EnvironmentUtil.arch)
    
    def __get_ability(self, library_json_entity: dict, platform: str) -> bool:
        linux: bool
        osx: bool
        windows = linux = osx = False
        for item in library_json_entity['rules']:
            if(item['action'] == "allow"):
                if(not 'os' in item):
                    windows = linux = osx = True
                    continue
                for enumerate2 in item['os'].values():
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
                if(not 'os' in item):
                    windows = linux = osx =False
                
                if ('os' in item):
                    for enumerate2 in item['os'].values():
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