from email.mime import image
import itertools
from pathlib import Path

import pytest
from slides2vid.core.project import Project

import logging

from slides2vid.converter.odp import ODPAudioConverter, ODPImageConverter
from slides2vid.converter.pdf import PDFImageConverter
from slides2vid.converter.pptx import PPTXAudioConverter
from slides2vid.core.video import FFMPEGVideoSlideGenerator
from slides2vid.tts.base import TTSEngine
from slides2vid.tts.chatterbox import ChatterboxTTS
from slides2vid.tts.gtts import GoogleTTS
logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


class Config:
    lang = "en"
    data_path = Path(f"test/data/{lang}")
    output_path = Path(f"test/output/{lang}") 
    output_path.mkdir(parents=True, exist_ok=True)
    audio_prompts_path = data_path / "voice_models"
    filenames = ["sample1","sample2"]
    engines = [ GoogleTTS(lang),]

class ConfigChatterbox(Config):
    def __init__(self) -> None:     
        self.engines = [ ChatterboxTTS(self.lang,"cpu"),
                         ChatterboxTTS(self.lang,"cpu",audio_prompt_path=self.audio_prompts_path/"sample1.mp3")]
    

def make_audio_converter(filepath:Path, work_path:Path,tts_engine:TTSEngine):
    if filepath.suffix == ".pptx":
        return PPTXAudioConverter(work_path,filepath,tts_engine)
    elif filepath.suffix == ".odp":
        return ODPAudioConverter(work_path,filepath,tts_engine)
    else:
        raise ValueError(f"Unsupported file type: {filepath.suffix}")
    
def make_image_converter(filepath:Path, work_path:Path):
    if filepath.suffix == ".pdf":
        return PDFImageConverter(work_path,filepath)
    elif filepath.suffix == ".odp":
        return ODPImageConverter(work_path,filepath)
    else:
        raise ValueError(f"Unsupported file type: {filepath.suffix}")    


def fixtures(c:Config,work_path:Path):
    audio_inputs = ["pptx","odp"]
    image_inputs = ["pdf","odp"]
    configs = itertools.product(c.filenames,c.engines,image_inputs,audio_inputs)
    for filename,engine,image_input,audio_input in configs:
        id = f"{filename}_{engine}_{image_input}_{audio_input}"
        fixture_work_path = work_path/id
        
        image_file = c.data_path/f"{filename}.{image_input}"
        image_converter = make_image_converter(image_file,fixture_work_path)
        audio_file = c.data_path/f"{filename}.{audio_input}"
        audio_converter = make_audio_converter(audio_file,fixture_work_path,engine)
        
        video_path = c.output_path/f"{id}.mp4"
        yield Project(id,fixture_work_path,
                        FFMPEGVideoSlideGenerator(fixture_work_path),
                        image_converter,
                        audio_converter,
                        video_path)


work_path = Path()/"test/work_folders"
simple_fixtures = list(fixtures(Config(),work_path))


@pytest.mark.parametrize("p",simple_fixtures)
def test_generation_simple(p:Project):
    work_path.mkdir(parents=True, exist_ok=True)
    p.work_path.mkdir(parents=True, exist_ok=True)
    p.run()
    assert p.video_path.exists()    
