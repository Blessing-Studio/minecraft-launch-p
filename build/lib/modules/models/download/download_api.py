class DownloadAPI():
    def __init__(self, host: str, version_manifest: str, assets: str, libraries: str):
        self.host = host
        self.version_manifest = version_manifest
        self.assets = assets
        self.libraries = libraries
