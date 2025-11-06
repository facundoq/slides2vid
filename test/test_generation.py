from pathlib import Path
import shutil

from click import prompt
import pytest
from slides2vid.core import Project

import logging

from slides2vid.preprocessor.odp import ODPAudioPreprocessor, ODPImagePreprocessor
from slides2vid.preprocessor.pdf import PDFImagePreprocessor
from slides2vid.preprocessor.pptx import PPTXAudioPreprocessor
from slides2vid.slides import FFMPEGSlideGenerator, SlideGenerator
from slides2vid.tts.base import TTSEngine
from slides2vid.tts.chatterbox import ChatterboxTTS
from slides2vid.tts.gtts import GoogleTTS
logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


def pdf_pptx_project(work_path:Path,pdf_path:Path,pptx_path:Path,video_path:Path,tts_engine:TTSEngine):
    
    generator = FFMPEGSlideGenerator(work_path)
    pdf_images = PDFImagePreprocessor(work_path,pdf_path)
    pptx_audios = PPTXAudioPreprocessor(work_path,tts_engine,pptx_path)
    p = Project(work_path,generator,pdf_images,pptx_audios,video_path)
    return p

data_path = Path("test/data")

engines = [GoogleTTS("en"),
            ChatterboxTTS("en","cpu"),
            ChatterboxTTS("en","cpu",audio_prompt_path=data_path/"messi.wav")]
 
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
