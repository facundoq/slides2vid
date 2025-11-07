from genericpath import exists
from re import sub
import subprocess
from slides2vid.converter.audio import AudioConverter
from slides2vid.converter.core import  Converter, ConverterResult


from pathlib import Path

from slides2vid.converter.pdf import PDFImageConverter
from slides2vid.tts.base import TTSEngine


class ODPImageConverter(Converter):
    LAST_MODIFIED_KEY = "last_modified"
    
    def __init__(self,work_path:Path,odt_path:Path) -> None:
        super().__init__(work_path)
        self.odt_path = odt_path
        
    
    def run(self)-> ConverterResult:
        file_changed = self.cache.file_changed(self.odt_path,self.LAST_MODIFIED_KEY)
        pdf_path = self.odt_path.with_suffix(".pdf")
        if file_changed or not pdf_path.exists():
            subprocess.run(f"soffice --headless --convert-to pdf {self.odt_path}",shell=True)
            self.cache.update_file_modification(self.odt_path,self.LAST_MODIFIED_KEY)
        pdf_preprocessor = PDFImageConverter(self.work_path,pdf_path)
        
        return pdf_preprocessor.run()
    

from odf.opendocument import load
from odf import draw, presentation, text

class ODPAudioConverter(AudioConverter):
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

    def run(self)-> ConverterResult:
        texts = self.get_slides_text()
        result = self.generate_audios(texts)
        return result
    
    