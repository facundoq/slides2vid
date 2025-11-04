

from email.mime import audio
from pathlib import Path
from .base import TTSEngine

import torchaudio as ta
from chatterbox.tts import ChatterboxTTS
from chatterbox.mtl_tts import ChatterboxMultilingualTTS


class ChatterboxTTS(TTSEngine):
    def __init__(self,device="cpu",audio_prompt_path:Path=None) -> None:
        super().__init__()
        self.device=device
        self.audio_prompt_path=audio_prompt_path

    def generate(self, text: str,path:Path,language:str):
        model = ChatterboxMultilingualTTS.from_pretrained(device=self.device)
        wav = model.generate(text, language_id=language,audio_prompt_path=self.audio_prompt_path)
        ta.save(path, wav, model.sr)