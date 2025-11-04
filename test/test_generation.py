from pathlib import Path
import shutil
import pytest
from slides2vid.core import Project

import logging

from slides2vid.preprocessor.pdf import PDFImagePreprocessor
from slides2vid.preprocessor.pptx import PPTXAudioPreprocessor
from slides2vid.tts.chatterbox import ChatterboxTTS
from slides2vid.tts.gtts import GoogleTTS
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

def test_generation(tmp_path):
    fixtures = [ 
            (GoogleTTS("en"),"gTTS"),
             (ChatterboxTTS("en","cpu"), "ChatterboxTTS")
                ] 
    files = ["sample1","sample2"]  
    for tts_engine, tts_name in fixtures:
        for filename in files:
            folder_path = Path("data")
            audios_path = folder_path/f"{filename}.pptx"
            images_path = folder_path/f"{filename}.pdf"
            video = folder_path/f"{filename}_{tts_name}.mp4"
            video.unlink(missing_ok=True)
            work_path = Path()/"test"/tts_name/f"{filename}"   
            # work
            #shutil.rmtree(work_path)
            work_path.mkdir(parents=True, exist_ok=True)
            p = Project(work_path)
            images = PDFImagePreprocessor(images_path,work_path)
            audios = PPTXAudioPreprocessor(audios_path,work_path,tts_engine)
            p.make_video(images,audios,video)
            assert video.exists()