

from abc import ABC, abstractmethod
from pathlib import Path


from slides2vid.converter.cache import Cache


class ConverterResult:
    
    @abstractmethod
    def __len__(self):
        raise NotImplementedError
    
    @abstractmethod
    def path(self,i)->Path:
        raise NotImplementedError
    
    @abstractmethod
    def changed(self,i)->bool:
        raise NotImplementedError

   
class BaseConverterResult(ConverterResult):
    def __init__(self,paths:list[Path],changed:list[bool]) -> None:
        assert len(paths) == len(changed)
        self.paths = paths
        self.changed_list = changed

    def __len__(self):
        return len(self.paths)
    def path(self,i)->Path:
        return self.paths[i]
    def changed(self,i)->bool:
        return self.changed_list[i]


class Converter(ABC):
    def __init__(self,work_path:Path) -> None:
        super().__init__()
        self.work_path = work_path
        self.cache = Cache(work_path,self)
        
    def run(self)->ConverterResult:
        raise NotImplementedError
    
    def finished(self,path:Path)->None:
        pass
    
    
