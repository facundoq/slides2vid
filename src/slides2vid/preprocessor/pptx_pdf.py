

from pathlib import Path
from slides2vid.core import Project
from slides2vid.preprocessor.core import Preprocessor


class PPTXPDFPreprocessor(Preprocessor):
    def __init__(self,pptx_path:Path,pdf_path:Path) -> None:
        super().__init__()
        self.pptx_path = pptx_path
        self.pdf_path = pdf_path
    
    def preprocess(self) -> Project:
        