from slides2vid.converter.core import BaseConverterResult,  Converter, ConverterResult
import tqdm
from pdf2image import convert_from_path,pdfinfo_from_path

from pathlib import Path


class PDFImageConverter(Converter):
    LAST_MODIFIED_KEY = "last_modified_pdf"

    def __init__(self,work_path:Path,pdf_path:Path) -> None:
        super().__init__(work_path)
        self.pdf_path = pdf_path

    def run(self)-> ConverterResult:
        n = pdfinfo_from_path(str(self.pdf_path.absolute()))["Pages"]
        image_paths = [self.work_path/f'frame_{i}.png' for i in range(n)]
        images_exist = all(map(lambda p: p.exists(),image_paths))
        file_changed = self.cache.file_changed(self.pdf_path,self.LAST_MODIFIED_KEY)
        if file_changed or not images_exist:
            images = convert_from_path(self.pdf_path)
            pbar = tqdm.tqdm(enumerate(images),total=n)
            pbar.set_description("Generating slide images")
            for i,image in pbar:
                image.save(image_paths[i])
            images_changed = [True]*n
        else:
            images_changed = [False]*n
        self.cache.update_file_modification(self.pdf_path,self.LAST_MODIFIED_KEY)
        
        return BaseConverterResult(image_paths,images_changed)