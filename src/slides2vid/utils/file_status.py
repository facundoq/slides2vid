from slides2vid.converter.cache import Cache


from abc import ABC
from pathlib import Path


class FileChangeStatus(ABC):
    def __init__(self,paths:list[Path],cache:Cache) -> None:
        self.paths = paths
        self.cache = cache
        # hashes are calculated only when needed
        self.hashes = None


    def get_file_hash(self,file:Path)->str:
        return file.stat().st_mtime_ns.__str__()

    def get_hashes(self)->dict[str,str]:
        hashes = {}
        for file in self.paths:
            hashes[str(file.absolute())] = self.get_file_hash(file)
        return hashes

    def get_changed(self)->list[bool]:
        self.hashes = self.get_hashes()
        hashes_str = {str(k):v for k,v in self.hashes.items()}
        def changed(path:str)->bool:
            cached_hash = self.cache.items.get(path,None)
            return cached_hash != hashes_str[path]
        return [changed(str(p)) for p in self.paths]

    def update_hashes_cache(self,paths:list[Path]=None)->None:
        if not self.hashes is None:
            if paths is None:
                paths = self.hashes.keys()
            selected_hashes = {str(p):self.hashes[str(p)] for p in paths}
            self.cache.update(selected_hashes)
            self.cache.save_cache()