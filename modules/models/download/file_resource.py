from minecraft_launch.modules.interface.iresource import IResource


class FileResource(IResource):
    def __init__(self, root: str, name: str, size: int, check_sum: str, url: str, file_info: str) -> None:
        self.root: str = root
        self.name: str = name
        self.size: int = size
        self.check_sum: str = check_sum
        self.url: str = url
        self.file_info: str = file_info

    def to_file_info(self):
        return self.file_info
    
