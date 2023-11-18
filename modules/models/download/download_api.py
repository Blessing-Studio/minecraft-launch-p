class DownloadAPI():
    def __init__(self, host: str, version_manifest: str, assets: str, libraries: str):
        self.host: str = host
        self.version_manifest: str = version_manifest
        self.assets: str = assets
        self.libraries: str = libraries
