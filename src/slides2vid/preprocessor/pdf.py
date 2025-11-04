from genericpath import exists
from slides2vid.preprocessor.core import BasePreprocessor, Cache


import tqdm
from pdf2image import convert_from_path,pdfinfo_from_path

import yaml

from pathlib import Path


class PDFImagePreprocessor(BasePreprocessor):
    LAST_MODIFIED_PDF_KEY = "last_modified_pdf"

    def __init__(self,pdf_path:Path,work_path:Path) -> None:
        self.cache = Cache(work_path,self,{self.LAST_MODIFIED_PDF_KEY:0.0})
        paths,changed = self.generate_images_from_pdf(pdf_path,work_path)
        super().__init__(paths,changed)

    def generate_images_from_pdf(self,pdf_path:Path,work_path:Path):
        pdf_stat = pdf_path.stat()
        modified_pdf = pdf_stat.st_mtime
        last_modified_pdf = self.cache[self.LAST_MODIFIED_PDF_KEY]
        n = pdfinfo_from_path(pdf_path)["Pages"]
        image_paths = [work_path/f'frame_{i}.png' for i in range(n)]
        images_exist = all(map(lambda p: p.exists(),image_paths))
        if modified_pdf != last_modified_pdf or not images_exist:
            images = convert_from_path(pdf_path)
            pbar = tqdm.tqdm(enumerate(images),total=n)
            pbar.set_description("Generating slide images")
            for i,image in pbar:
                image.save(image_paths[i])
            images_changed = [True]*n
        else:
            images_changed = [False]*n

        self.cache.update({self.LAST_MODIFIED_PDF_KEY:modified_pdf})
        return image_paths,images_changed