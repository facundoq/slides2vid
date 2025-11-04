

from abc import ABC, abstractmethod
from pathlib import Path


class TTSEngine(ABC):

    @abstractmethod
    def generate(self, text: str,path:Path):
        raise NotImplementedError