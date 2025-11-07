from abc import ABC, abstractmethod
from pathlib import Path

from slides2vid.converter.core import Converter, ConverterResult
import subprocess

class FolderConverter(Converter):
    def __init__(self,work_path:Path,folderpath:Path,file_extensions:list[str]):
        super().__init__(work_path)
        self.folderpath = folderpath
        self.file_extensions = file_extensions
        self.hashes = None
    
    def get_file_hash(self,file:Path)->str:
        return file.stat().st_mtime_ns.__str__()
    
    def get_hashes(self,paths:list[Path])->dict[str,str]:
        hashes = {}
        for file in paths:
            hashes[str(file.absolute())] = self.get_file_hash(file)
        return hashes
    
    def get_changed(self,paths:list[Path],hashes:dict[Path,str])->list[bool]:
        hashes_str = {str(k):v for k,v in hashes.items()}
        def changed(path:str)->bool:
            cached_hash:str = self.cache.items.get(path,None)
            return cached_hash == hashes_str[path]
        
        return [changed(str(p)) for p in paths]
    
    def update_hashes(self,hashes:dict[Path,str])->None:
        self.cache.update(hashes)
        self.cache.save_cache()
        
    def run(self)-> ConverterResult:
        paths = sorted([file for file in self.folderpath.iterdir() if file.suffix in self.file_extensions])
        self.hashes = self.get_hashes(paths)
        changed = self.get_changed(paths,self.hashes)
        return ConverterResult(paths, changed)
        
    def finished(self,path:Path)->None:
        path : str = str(path.absolute)
        hash = self.hashes[path]
        self.cache.update({self.hashes[path]:hash})
        self.cache.save_cache()
    