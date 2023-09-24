from typing import Iterable
from minecraft_launch.modules.enum.launch_state import LaunchState


class MinecraftLaunchResponse():
    def __init__(self, state: LaunchState, args: Iterable[str], exception: Exception|None = None):
        self.state: LaunchState = state
        self.arguemnts: Iterable[str] = args
        self.exception: Exception|None = exception