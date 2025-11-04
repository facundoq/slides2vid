from pathlib import Path
import shutil

from click import prompt
import pytest
from slides2vid.core import Project

import logging

from slides2vid.preprocessor.pdf import PDFImagePreprocessor
from slides2vid.preprocessor.pptx import PPTXAudioPreprocessor
from slides2vid.tts.chatterbox import ChatterboxTTS
from slides2vid.tts.gtts import GoogleTTS
logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)

def test_generation(tmp_path):
    # audio_prompt_path = Path("~/messi.wav")
    audio_prompt_path = Path("data/facu-en.wav")
    fixtures = [ 
          #  (GoogleTTS("en"),"gTTS"),
             (ChatterboxTTS("en","cuda",audio_prompt_path=audio_prompt_path), "ChatterboxTTS-facu",)
                ] 
    files = ["sample1"]  
    for tts_engine, fixture_name in fixtures:
        for filename in files:
            print(f"Testing {fixture_name} with {filename}")
            folder_path = Path("data")
            audios_path = folder_path/f"{filename}.pptx"
            images_path = folder_path/f"{filename}.pdf"
            video = folder_path/f"{filename}_{fixture_name}.mp4"
            video.unlink(missing_ok=True)
            work_path = Path()/"test"/fixture_name/f"{filename}"   
            # work
            #shutil.rmtree(work_path)
            work_path.mkdir(parents=True, exist_ok=True)
            p = Project(work_path)
            images = PDFImagePreprocessor(images_path,work_path)
            audios = PPTXAudioPreprocessor(audios_path,work_path,tts_engine)
            p.make_video(images,audios,video)
            assert video.exists()