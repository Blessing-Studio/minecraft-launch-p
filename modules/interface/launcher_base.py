from typing import TypeVar, Generic
from minecraft_launch.modules.models.launch.launch_config import LaunchConfig
from abc import ABCMeta


T = TypeVar('T')
T2 = TypeVar('T2')
class LauncherBase(Generic[T, T2]):
    def __init__(self) -> None:
        self.launch_setting: LaunchConfig
        self.arguments_builder: T

    def launch(self, id: str) -> T2:
        raise Exception()