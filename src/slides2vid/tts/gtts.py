

from pathlib import Path
from .base import TTSEngine
from gtts import gTTS

class GoogleTTS(TTSEngine):
    def generate(self, text: str,path:Path,language:str):
        tts = gTTS(text,lang=language)
        tts.save(str(path))