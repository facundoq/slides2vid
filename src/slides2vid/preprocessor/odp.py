from genericpath import exists
from re import sub
import subprocess
from slides2vid.preprocessor.audio import AudioPreprocessor
from slides2vid.preprocessor.core import  Preprocessor, PreprocessorResult


import tqdm
from pdf2image import convert_from_path,pdfinfo_from_path

import yaml

from pathlib import Path

from slides2vid.preprocessor.pdf import PDFImagePreprocessor
from slides2vid.tts.base import TTSEngine


class ODPImagePreprocessor(Preprocessor):
    LAST_MODIFIED_KEY = "last_modified"
    
    def __init__(self,work_path:Path,odt_path:Path) -> None:
        super().__init__(work_path)
        self.odt_path = odt_path
        
    
    def run(self)-> PreprocessorResult:
        file_changed = self.cache.file_changed(self.odt_path,self.LAST_MODIFIED_KEY)
        pdf_path = self.odt_path.with_suffix(".pdf")
        if file_changed or not pdf_path.exists():
            subprocess.run(f"soffice --headless --convert-to pdf {self.odt_path}",shell=True)
        pdf_preprocessor = PDFImagePreprocessor(self.work_path,pdf_path)
        self.cache.update_file_modification(self.odt_path,self.LAST_MODIFIED_KEY)
        return pdf_preprocessor.run()
    

from odf.opendocument import load
from odf import draw, presentation, text

class ODPAudioPreprocessor(AudioPreprocessor):
    LAST_MODIFIED_KEY = "last_modified"
    
    def __init__(self,work_path:Path,odt_path:Path,engine:TTSEngine) -> None:
        super().__init__(work_path,engine)
        self.odt_path = odt_path
        
    def get_slides_text(self)->dict[int,str]:
        doc = load(self.odt_path)
        notes_by_slide = {}
        # Each slide is a draw.Page element 
        for i,page in enumerate(doc.getElementsByType(draw.Page)):
            notes = page.getElementsByType(presentation.Notes)
            notes_text = ""
            for note in notes:
                notes_text += f"{note}\n"
            notes_by_slide[i+1] = notes_text.strip()        
        return notes_by_slide

    def run(self)-> PreprocessorResult:
        texts = self.get_slides_text()
        changed = self.get_changed(texts)
        result = self.generate_audios(texts,changed)
        self.update_texts_cache(texts)
        return result
    
    