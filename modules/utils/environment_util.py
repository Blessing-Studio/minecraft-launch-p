import platform


class EnvironmentUtil():
    arch: str = "64" if platform.architecture()[0] == "64bit" else "32"

    is_mac: bool = True if platform.system() == "Darwin" else False
    is_linux: bool = True if platform.system() == "Linux" else False
    is_windows: bool = True if platform.system() == "Windows" else False

    @staticmethod
    def get_platform_name() -> str:
        if(platform.system() == "Darwin"):
            return "osx"
        if(platform.system() == "Linux"):
            return "linux"
        if(platform.system() == "Windows"):
            return "windows"
        return "unknown"