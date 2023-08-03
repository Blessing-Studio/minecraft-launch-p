from typing import TypeVar, Generic
from modules.models.launch.launch_config import LaunchConfig


T = TypeVar('T')
T2 = TypeVar('T2')
class LaunchBase(Generic[T, T2]):
    def __init__(self) -> None:
        self.launch_setting: LaunchConfig
        self.arguments_builder: T

    def launch_task_async(self, id: str) -> T2:
        raise Exception()