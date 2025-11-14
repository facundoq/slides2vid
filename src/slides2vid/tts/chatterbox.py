

from email.mime import audio
from pathlib import Path
from .base import TTSEngine

import torchaudio as ta
from chatterbox.tts import ChatterboxTTS
from chatterbox.mtl_tts import ChatterboxMultilingualTTS, SUPPORTED_LANGUAGES

CHATTERBOX_LANGUAGES = SUPPORTED_LANGUAGES

class ChatterboxTTS(TTSEngine):
    def __init__(self,language:str,device="cpu",audio_prompt_path:Path=None) -> None:
        super().__init__(language)
        self.device=device
        self.audio_prompt_path=audio_prompt_path
        self.language = language
        self.model = None

    def __str__(self) -> str:
        prompt = self.audio_prompt_path.name.split(".")[0] if self.audio_prompt_path is not None else "no_prompt"
        return f"{self.__class__.__name__}_{self.language}_{self.device}_{prompt}"
    
    def generate(self, text: str,path:Path,):
        if self.model is None:
            self.model = ChatterboxMultilingualTTS.from_pretrained(device=self.device)
        wav = self.model.generate(text, language_id=self.language,audio_prompt_path=self.audio_prompt_path)
        ta.save(path, wav, self.model.sr)