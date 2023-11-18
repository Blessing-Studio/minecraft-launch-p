class IResource():
    def __init__(self) -> None:
        self.root: str
        self.name: str
        self.size: int
        self.check_sum: str
    
    def to_file_info() -> str:
        ...