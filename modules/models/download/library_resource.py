class LibraryResource():
    def __init__(self) -> None:
        self.root: str
        self.check_sum: str
        self.size: int
        self.url: str
        self.name: str
        self.is_enable: bool
        self.is_natives: bool = False

    def to_file_info(self) -> str:
        root: str = f"{self.root}\\libraries"
        for item in self.format_name(self.name):
            root = f"{root}\\{item}"
        return root

    @staticmethod
    def format_name(name: str) -> list[str]:
        extension: list[str] = name.split('@') if '@' in name else []
        sub_string: list[str] = name.replace(f"@{extension[1]}", "").split(':') if any(extension) else name.split(':')
        array: list[str] = sub_string[0].split('.')
        for i in range(len(array)):
            yield array[i]
        yield sub_string[1]
        yield sub_string[2]
        if (not any(extension)):
            yield f"{sub_string[1]}-{sub_string[2]}{'-' + sub_string[3] if len(sub_string) > 3 else ''}.jar"
        else:
            yield f"{sub_string[1]}-{sub_string[2]}{'-' + sub_string[3] if len(sub_string) > 3 else ''}.jar".replace("jar", extension[1])
