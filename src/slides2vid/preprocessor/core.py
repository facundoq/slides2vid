

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import yaml


class PreprocessorResult:
    
    @abstractmethod
    def __len__(self):
        raise NotImplementedError
    
    @abstractmethod
    def path(self,i)->Path:
        raise NotImplementedError
    
    @abstractmethod
    def changed(self,i)->bool:
        raise NotImplementedError

   
class BasePreprocessorResult(PreprocessorResult):
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


class Preprocessor(ABC):
    def __init__(self,work_path:Path) -> None:
        super().__init__()
        self.work_path = work_path
        self.cache = Cache(work_path,self)
        
    def run(self)->PreprocessorResult:
        raise NotImplementedError
    
    def mark_processed(self,path:Path)->None:
        pass
    
class Cache:
    def __init__(self,work_path:Path,obj:Any,cache={}) -> None:
        self.cache_path = work_path/ f"{obj.__class__.__name__}_cache.yaml"
        self.load_cache(cache)
    
    
    def file_changed(self,file_path:Path,cache_key:str)->bool:
        file_stat = file_path.stat()
        modified_time = file_stat.st_mtime
        last_modified_time = self.items.get(cache_key,0.0)
        return modified_time != last_modified_time
    
    def update_file_modification(self,file_path:Path,cache_key:str)->None:
        file_stat = file_path.stat()
        modified_time = file_stat.st_mtime
        self.items[cache_key]=modified_time
        self.save_cache()
        
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
    def get(self,key:str,default:Any=None)->Any:
        return self.items.get(key,default)
    
    def load_cache(self,default:dict[str,Any]):
        if self.cache_path.exists():
            with open(self.cache_path, 'r') as file:
                self.items= yaml.safe_load(file)  
        else:
            self.items = default
    
