from genericpath import exists
import logging
from slides2vid.preprocessor.core import BasePreprocessor, Cache


import tqdm
from pdf2image import convert_from_path

import yaml

from pathlib import Path
from pptx import Presentation
from slides2vid.tts.base import TTSEngine

logger = logging.getLogger(__name__)

class PPTXAudioPreprocessor(BasePreprocessor):
    TEXTS_KEY = "texts"

    def __init__(self,pptx_path:Path,work_path:Path,engine:TTSEngine) -> None:
        self.cache = Cache(work_path,self,{self.TEXTS_KEY:{}})
        paths,changed = self.generate_audios_from_pptx(pptx_path,work_path,engine)
        super().__init__(paths,changed)

    def generate_audios_from_pptx(self,pptx_path:Path,work_path:Path,engine:TTSEngine):
        presentation = Presentation(pptx_path)
        n = len(presentation.slides)
        texts = self.cache[self.TEXTS_KEY]
        paths = [work_path/f'frame_{i}.mp3' for i in range(n)]
        changed = [True for i in range(n)]
        pbar = tqdm.tqdm(enumerate(presentation.slides),total=n)
        pbar.set_description("Generating slide audios")
        for i,slide in pbar:
            if slide.has_notes_slide:
                text = slide.notes_slide.notes_text_frame.text
            else:
                text = ""
            logger.info(f"Slide {i} text:\n {text}\n")
            audio_changed = True
            if i in texts:
                previous_notes = texts[i]
                audio_path = paths[i]
                if previous_notes == text and audio_path.exists():
                    logger.info(f"Slide {i} text did not change, skipping audio generation.")
                    audio_changed = False
                    changed[i] = audio_changed
            if audio_changed:
                engine.generate(text,paths[i])
            texts[i]=text
        
        self.cache.update({self.TEXTS_KEY:texts}) 

        return paths,changed