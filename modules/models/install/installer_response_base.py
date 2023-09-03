class InstallerResponseBase():
    def __init__(self):
        self.exception: Exception
        self.success: bool