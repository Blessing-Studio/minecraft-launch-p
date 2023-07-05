class LaunchConfig():
    def __init__(self, account, jvmConfig: list, gameWindowConfig: list, severConfig = None):
        self.Account = account
        self.JvmConfig = jvmConfig
        self.GameWindowConfig = gameWindowConfig
        self.ServerConfig = severConfig
