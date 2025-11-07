from pathlib import Path
import shutil

from click import prompt
import pytest
from slides2vid.core import Project

import logging

from slides2vid.converter.odp import ODPAudioConverter, ODPImageConverter
from slides2vid.converter.pdf import PDFImageConverter
from slides2vid.converter.pptx import PPTXAudioConverter
from slides2vid.slides import FFMPEGSlideGenerator, SlideGenerator
from slides2vid.tts.base import TTSEngine
from slides2vid.tts.chatterbox import ChatterboxTTS
from slides2vid.tts.gtts import GoogleTTS
logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)

data_path = Path("test/data")

engines = [ GoogleTTS("en"),
            ChatterboxTTS("en","cpu"),
            ChatterboxTTS("en","cpu",audio_prompt_path=data_path/"messi.wav")]

def audio_converters(filename:str, work_path:Path,tts_engine:TTSEngine,pptx_path:Path):
    
    return [
        PPTXAudioConverter(work_path,data_path/f"{filename}.pptx",tts_engine),
        ODPAudioConverter(work_path,data_path/f"{filename}.odp",tts_engine),
    ]
    

def image_converters(filename:str, work_path:Path):
    
    return [
        PDFImageConverter(work_path,data_path/f"{filename}.pdf"),
        ODPImageConverter(work_path,data_path/f"{filename}.odp"),
    ]
    
def pdf_pptx_project(work_path:Path,pdf_path:Path,pptx_path:Path,video_path:Path,tts_engine:TTSEngine):
    
    generator = FFMPEGSlideGenerator(work_path)
    pdf_images = PDFImageConverter(work_path,pdf_path)
    pptx_audios = PPTXAudioConverter(work_path,tts_engine,pptx_path)
    p = Project(work_path,generator,pdf_images,pptx_audios,video_path)
    return p


 
def pdf_pptx_project_fixtures(work_path:Path):
    filename = "sample2"
    for engine in engines:
        id = f"{engine}_{filename}"
        fixture_work_path = work_path/id
        audios_path = data_path/f"{filename}.pptx"
        images_path = data_path/f"{filename}.pdf"
        video_path = fixture_work_path/f"output.mp4"
        yield pdf_pptx_project(fixture_work_path,images_path,audios_path,video_path,engine)

# def odt_fixtures(work_path:Path):
#     filename = "test.odt"
#     for engine in engines:
#         odt_path = data_path/"{filename}.odt"
#         id = f"{engine}_{filename}"
#         images = ODPImagePreprocessor(work_path,odt_path)    
#         audios = ODPAudioPreprocessor(work_path,odt_path,engine)
#         generator = FFMPEGSlideGenerator(work_path)
#         p = Project(work_path,generator,images,audios,)

def project_fixtures(work_path:Path):
    return  list(pdf_pptx_project_fixtures(work_path))

def test_generation(tmp_path):
    
    work_path = Path()/"test/work_folders"
    work_path.mkdir(parents=True, exist_ok=True)
    for p in project_fixtures(work_path):
        #shutil.rmtree(p.work_path)
        p.work_path.mkdir(parents=True, exist_ok=True)
        p.run()
        assert p.video_path.exists()    
