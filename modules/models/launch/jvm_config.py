class JvmConfig():
    def __init__(self, file, max_memory: int = 1024, min_memory: int = 512) -> None:
        self.java_path: str = file
        self.max_memory: int = max_memory
        self.min_memory: int = min_memory
        self.used_gc: bool = True
        self.advanced_arguments: list[str]|None = None
        self.gc_arguments: list[str]|None = None