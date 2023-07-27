class FileResource():
    def __init__(self, root: str, name: str, size: int, check_sum: str, url: str, file_info) -> None:
        self.root = root
        self.name = name
        self.size = size
        self.check_sum = check_sum
        self.url = url
        self.file_info = file_info

    def to_file_info(self):
        return self.file_info
    
