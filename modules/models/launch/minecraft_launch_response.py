from minecraft_launch.modules.enum.launch_state import LaunchState


class MinecraftLaunchResponse():
    def __init__(self, state: LaunchState, args: list[str], exception: Exception|None = None):
        self.state = state
        self.arguemnts = args
        self.exception = exception