from modules.enum.launch_state import LaunchState


class MinecraftLaunchResponse():
    def __init__(self, state: LaunchState, args: list[str]):
        self.state = state
        self.arguemnts = args
        if(state == LaunchState.Success):
            ...

