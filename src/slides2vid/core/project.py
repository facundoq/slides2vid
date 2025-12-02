import tqdm
from pathlib import Path

from .. import Converter
from .video import  SlideGenerator

# from yamlable import YamlAble, yaml_info
import logging
logger = logging.getLogger(__name__)

FFMPEG_NAME = 'ffmpeg'

class Project:
    project_filename = "project.yaml"

    @property
    def project_config_path(self):
        return self.work_path / self.project_filename
    
    def __init__(self, id:str,work_folder:Path,generator:SlideGenerator,images_preprocessor:Converter, audios_preprocessor:Converter,video_path:Path,verbose=False) -> None:
        self.id=id
        self.generator = generator
        self.images_converter = images_preprocessor
        self.audios_converter = audios_preprocessor
        self.work_path = work_folder
        self.video_path = video_path
        self.verbose=verbose
    
    
    def run(self,):
        video_paths = self.generate_videos()
        #self.save_project()
        logger.info("Concatenating slide videos...")
        self.generator.concatenate(video_paths,self.video_path)
        logger.info(" done.")
        
    def generate_videos(self):
        # TODO paralellize
        if self.verbose:
            print("Generating images...")
        images_paths,images_changed = self.images_converter.run()
        if self.verbose:
            print("Generating audios...")
        audios_paths,audios_changed = self.audios_converter.run()
        assert len(images_paths) == len(audios_paths)
        n = len(images_paths)
        video_paths = [self.work_path / f"frame_{i}.mp4" for i in range(n)]
        
        pbar = tqdm.trange(n)
        pbar.set_description("Generating slide videos")
        for i in pbar:
            if images_changed[i] or audios_changed[i]:
                # TODO: parallelize
                # TODO: replace audio if image did not change? or sth similar
                self.generator.generate(images_paths[i], audios_paths[i],video_paths[i])
        self.images_converter.finished(images_paths)
        self.audios_converter.finished(audios_paths)
        return video_paths
        


