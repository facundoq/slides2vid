import faulthandler
from fileinput import filename
from tkinter import LAST

import tqdm
from pathlib import Path

from subprocess import run

from pdf2image import convert_from_path,pdfinfo_from_path

from gtts import gTTS
from slides2vid.preprocessor.core import Preprocessor
from slides2vid.slides import FFMPEGSlideGenerator, SlideGenerator

# from yamlable import YamlAble, yaml_info
import yaml
import logging
logger = logging.getLogger(__name__)

FFMPEG_NAME = 'ffmpeg'

class Project:
    project_filename = "project.yaml"

    @property
    def project_config_path(self):
        return self.work_path / self.project_filename
    
    def __init__(self, work_folder:Path):
        self.work_path = work_folder
                
    def generate_videos(self,generator:SlideGenerator,images:Preprocessor,audios:Preprocessor):
        assert len(images) == len(audios)
        n = len(images)
        video_paths = [self.work_path / f"frame_{i}.mp4" for i in range(n)]

        pbar = tqdm.trange(n)
        pbar.set_description("Generating slide videos")
        for i in pbar:
            if images.changed(i) or audios.changed(i):
                # TODO: parallelize
                # TODO: replace audio if image did not change? or sth similar
                generator.generate(images.path(i), audios.path(i),video_paths[i])
        return video_paths

        
    def make_video(self, images:Preprocessor,audios:Preprocessor, output_path:Path):
        generator = FFMPEGSlideGenerator(self.work_path)
        video_paths = self.generate_videos(generator,images,audios)
        #self.save_project()
        logger.info("Concatenating slide videos...")
        generator.concatenate(video_paths,output_path)
        logger.info(" done.")

