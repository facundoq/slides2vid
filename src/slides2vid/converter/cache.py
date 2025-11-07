import yaml


from pathlib import Path
from typing import Any


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