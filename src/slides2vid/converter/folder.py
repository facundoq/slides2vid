from abc import abstractmethod
from pathlib import Path

from slides2vid.utils.file_status import FileChangeStatus
from . import Converter,ConverterResult
import subprocess


class FilesConverter(Converter):
    def __init__(self,work_path:Path,paths:list[Path],verbose=False) -> None:
        super().__init__(work_path,verbose)
        self.paths = paths
        self.status = FileChangeStatus(self.paths,self.cache)
 
    def run(self)-> ConverterResult:
        changed = self.status.get_changed()
        
        return self.paths, changed
    def finished(self, paths: list[Path]) -> None:
        self.status.update_hashes_cache(paths)

class FolderConverter(Converter):
    def __init__(self,work_path:Path,folderpath:Path,file_extensions:list[str],verbose=False) -> None:
        super().__init__(work_path,verbose)
        self.folderpath = folderpath
        self.file_extensions = file_extensions

    def run(self)-> ConverterResult:
        # paths are recalculated each time since folder contents can change
        paths = sorted([file for file in self.folderpath.iterdir() if file.suffix in self.file_extensions])
        self.status = FileChangeStatus(paths,self.cache)
        changed = self.status.get_changed()
        return paths, changed
    
    def finished(self, paths: list[Path]) -> None:
        if not self.status is None:
            self.status.update_hashes_cache(paths)

class ImageFolderConverter(FolderConverter):
    EXTENSIONS = [".jpg",".jpeg",".png",".gif"]
    def __init__(self,work_path:Path,folderpath:Path,verbose=False) -> None:
        super().__init__(work_path,folderpath,ImageFolderConverter.EXTENSIONS,verbose)


class AudioFolderConverter(FolderConverter):
    EXTENSIONS = [".mp3",".m4a",".aac",".wav"]
    def __init__(self,work_path:Path,folderpath:Path,verbose=False) -> None:
        super().__init__(work_path,folderpath,AudioFolderConverter.EXTENSIONS,verbose)

