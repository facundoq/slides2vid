

from abc import ABC, abstractmethod
from pathlib import Path


class TTSEngine(ABC):
    def __init__(self,language:str) -> None:
        super().__init__()
        self.language = language
    @abstractmethod
    def generate(self, text: str,path:Path):
        raise NotImplementedError