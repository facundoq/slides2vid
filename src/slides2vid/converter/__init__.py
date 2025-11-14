from slides2vid.converter.cache import Cache


from abc import abstractmethod
from pathlib import Path



type ConverterResult = tuple[list[Path],list[bool]]

from abc import ABC
from pathlib import Path


class Converter(ABC):
    def __init__(self,work_path:Path,verbose=False) -> None:
        super().__init__()
        self.work_path = work_path
        self.verbose=verbose
        self.cache = Cache(work_path,self)

    def run(self)->ConverterResult:
        raise NotImplementedError

    def finished(self,paths:list[Path])->None:
        pass