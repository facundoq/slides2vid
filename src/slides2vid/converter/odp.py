from pathlib import Path
import subprocess
import typing
from odf.opendocument import load
from odf import draw, presentation

from . import  ConverterResult,Converter
from slides2vid.converter.audio import AudioConverter
from slides2vid.converter.pdf import PDFImageConverter
from slides2vid.tts.base import TTSEngine

from slides2vid.utils import tool



class ODPImageConverter(Converter):
    LAST_MODIFIED_KEY = "last_modified"
    
    def __init__(self,work_path:Path,odp_path:Path,verbose=False,force=False) -> None:
        super().__init__(work_path,verbose,force)
        tool.check_soffice_installed()
        self.odp_path = odp_path
        self.pdf_preprocessor = None
    
    def run(self)-> ConverterResult:
        file_changed = self.cache.file_changed(self.odp_path,self.LAST_MODIFIED_KEY)
        pdf_path = self.odp_path.with_suffix(".pdf")
        pdf_path = self.work_path/pdf_path.name
        if file_changed or not pdf_path.exists():
            args = ["--convert-to", "pdf", f"{self.odp_path}","--outdir",  f"{self.work_path}"]
            if self.verbose:
                print(f"Converting ODP to PDF with soffice: {' '.join(args)}")
            tool.soffice(args)
            if not pdf_path.exists():
                raise tool.ToolError(f"Failed to convert {self.odp_path} to PDF, args: {args}")
        self.pdf_preprocessor = PDFImageConverter(self.work_path,pdf_path)
        return self.pdf_preprocessor.run()
    
    def finished(self, paths: list[Path]) -> None:
        if not self.pdf_preprocessor is None:
            self.pdf_preprocessor.finished(paths)
        self.cache.update_file_modification(self.odp_path,self.LAST_MODIFIED_KEY)



class ODPAudioConverter(AudioConverter):
    
    def __init__(self,work_path:Path,odt_path:Path,engine:TTSEngine,verbose=False,force=False) -> None:
        super().__init__(work_path,engine,verbose,force)
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
        return self.generate_audios(texts)
    
    