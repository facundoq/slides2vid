

from abc import ABC, abstractmethod
from os import path
from pathlib import Path
from typing import Any

import yaml

class Preprocessor(ABC):

    @abstractmethod
    def __len__(self):
        raise NotImplementedError
    
    @abstractmethod
    def path(self,i)->Path:
        raise NotImplementedError
    
    @abstractmethod
    def changed(self,i)->bool:
        raise NotImplementedError
    
class BasePreprocessor(Preprocessor):
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
    
class Cache:
    def __init__(self,work_path:Path,obj:Any,cache={}) -> None:
        self.cache_path = work_path/ f"{obj.__class__.__name__}_cache.yaml"
        self.load_cache(cache)
    
    def update(self,items:dict[str,Any]):
        self.items = items
        self.save_cache()

    def save_cache(self,):
        with open(self.cache_path, 'w') as file:
            yaml.dump(self.items,file) 
    def __setitem__(self, key, item):
        self.items[key] = item
    def __getitem__(self, key):
        return self.items[key]
    
    def load_cache(self,default:dict[str,Any]):
        if self.cache_path.exists():
            with open(self.cache_path, 'r') as file:
                self.items= yaml.safe_load(file)  
        else:
            self.items = default
    
