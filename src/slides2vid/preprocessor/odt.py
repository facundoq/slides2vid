from genericpath import exists
from re import sub
import subprocess
from slides2vid.preprocessor.core import  Preprocessor, PreprocessorResult


import tqdm
from pdf2image import convert_from_path,pdfinfo_from_path

import yaml

from pathlib import Path

from slides2vid.preprocessor.pdf import PDFImagePreprocessor


class ODTImagePreprocessor(Preprocessor):
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
    