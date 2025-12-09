

from pathlib import Path
from .base import TTSEngine

import torchaudio as ta
from chatterbox.tts import ChatterboxTTS
from chatterbox.mtl_tts import ChatterboxMultilingualTTS, SUPPORTED_LANGUAGES

CHATTERBOX_LANGUAGES = SUPPORTED_LANGUAGES
from dataclasses import dataclass

@dataclass
class ChatterboxTTSConfig:
    audio_prompt_path:Path=None
    exaggeration:float=0.5
    cfg_weight:float=0.5
    temperature:float=0.8

    def as_dict(self):
        d = {
        "exaggeration":self.exaggeration,
         "cfg_weight":self.cfg_weight,
         "temperature":self.temperature,
         }
        if self.audio_prompt_path is not None:
            d["audio_prompt"] = self.audio_prompt_path
        return d
        
    def __str__(self) -> str:
        
        if self.audio_prompt_path is not None:
            prompt = self.audio_prompt_path.name.split(".")[0] 
        else:
            prompt = ""
        
        return f"C(p{prompt}_e{self.exaggeration}_c{self.cfg_weight}_t{self.temperature})"
        
class ChatterboxTTS(TTSEngine):
    def __init__(self,language:str,device="cpu", config=ChatterboxTTSConfig()) -> None:
        super().__init__(language)
        self.device=device
        self.language = language
        self.model = None
        self.config = config

    def __str__(self) -> str:
        return f"{self.__class__.__name__}_{self.language}_{self.device}_{self.config}"
    
    def generate(self, text: str,path:Path,):
        if self.model is None:
            self.model = ChatterboxMultilingualTTS.from_pretrained(device=self.device)
        wav = self.model.generate(text, language_id=self.language, **self.config.as_dict()) 
        ta.save(path, wav, self.model.sr)