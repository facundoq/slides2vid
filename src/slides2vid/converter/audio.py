import tqdm

from . import Converter,ConverterResult
from pathlib import Path
from slides2vid.tts.base import TTSEngine

import logging
logger = logging.getLogger(__name__)

class AudioConverter(Converter):
    TEXTS_KEY = "texts"
    
    def __init__(self,work_path:Path,engine:TTSEngine,verbose=False) -> None:
        super().__init__(work_path,verbose)
        self.engine=engine
        
    def get_texts_cache(self)->dict[int,str]:
        return self.cache.get(self.TEXTS_KEY,default={})
    
    def update_texts_cache(self,texts:dict[int,str])->None:
        self.cache.update({self.TEXTS_KEY:texts})
        self.cache.save_cache()
    
    def get_changed(self,texts:dict[int,str])->dict[int,bool]:
        texts_cache = self.get_texts_cache()
        changed = {i:(texts[i] != texts_cache.get(i, "")) for i in texts}
        return changed
    
    def generate_audios(self,texts:dict[int,str])->ConverterResult:
        #TODO: add engine support for parallelization
        changed_texts = self.get_changed(texts)
        paths = []
        changed_audios = []
        pbar = tqdm.tqdm(enumerate(texts.items()),total=len(texts))
        pbar.set_description("Generating slide audios")
        for _,(i,text) in pbar:
            audio_path = self.work_path/f'frame_{i}.mp3'
            paths.append(audio_path)
            if changed_texts[i] or not audio_path.exists():
                self.engine.generate(text,audio_path)
                changed_audios.append(True)
            else:
                logger.info(f"Slide {i} text did not change, skipping audio generation.")
                changed_audios.append(False)
        self.update_texts_cache(texts)        
        return paths,changed_audios

    
    