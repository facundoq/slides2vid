

from pathlib import Path
from .base import TTSEngine
from gtts import gTTS

class GoogleTTS(TTSEngine):
    
    def generate(self, text: str,path:Path):
        tts = gTTS(text,lang=self.language)
        tts.save(str(path))