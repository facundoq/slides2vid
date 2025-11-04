

from email.mime import audio
from pathlib import Path
from .base import TTSEngine

import torchaudio as ta
from chatterbox.tts import ChatterboxTTS
from chatterbox.mtl_tts import ChatterboxMultilingualTTS


class ChatterboxTTS(TTSEngine):
    def __init__(self,language:str,device="cpu",audio_prompt_path:Path=None) -> None:
        super().__init__(language)
        self.device=device
        self.audio_prompt_path=audio_prompt_path
        self.language = language

    def generate(self, text: str,path:Path,):
        model = ChatterboxMultilingualTTS.from_pretrained(device=self.device)
        wav = model.generate(text, language_id=self.language,audio_prompt_path=self.audio_prompt_path)
        ta.save(path, wav, model.sr)