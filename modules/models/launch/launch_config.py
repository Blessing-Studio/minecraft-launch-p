class LaunchConfig():
    def __init__(self, account, jvm_config: list, game_window_config: list, sever_config = None):
        self.account = account
        self.jvm_config = jvm_config
        self.game_window_config = game_window_config
        self.server_config = sever_config