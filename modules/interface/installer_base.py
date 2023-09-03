from typing import TypeVar, Generic
from abc import ABC, abstractmethod


T = TypeVar('T')

class InstallerBase(Generic[T], ABC):
    @abstractmethod
    async def install(self) -> T:
        ...