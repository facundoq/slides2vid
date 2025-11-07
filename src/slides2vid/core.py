import tqdm
from pathlib import Path

from slides2vid.converter.core import Converter
from slides2vid.slides import  SlideGenerator

# from yamlable import YamlAble, yaml_info
import logging
logger = logging.getLogger(__name__)

FFMPEG_NAME = 'ffmpeg'

class Project:
    project_filename = "project.yaml"

    @property
    def project_config_path(self):
        return self.work_path / self.project_filename
    
    def __init__(self, work_folder:Path,generator:SlideGenerator,images_preprocessor:Converter, audios_preprocessor:Converter,video_path:Path) -> None:
        self.generator = generator
        self.images_preprocessor = images_preprocessor
        self.audios_preprocessor = audios_preprocessor
        self.work_path = work_folder
        self.video_path = video_path
    
    
    def run(self,):
        video_paths = self.generate_videos()
        #self.save_project()
        logger.info("Concatenating slide videos...")
        self.generator.concatenate(video_paths,self.video_path)
        logger.info(" done.")
        
    def generate_videos(self):
        # TODO paralellize
        images = self.images_preprocessor.run()
        audios = self.audios_preprocessor.run()
        assert len(images) == len(audios)
        n = len(images)
        video_paths = [self.work_path / f"frame_{i}.mp4" for i in range(n)]
        
        pbar = tqdm.trange(n)
        pbar.set_description("Generating slide videos")
        for i in pbar:
            if images.changed(i) or audios.changed(i):
                # TODO: parallelize
                # TODO: replace audio if image did not change? or sth similar
                self.generator.generate(images.path(i), audios.path(i),video_paths[i])
        return video_paths

        


