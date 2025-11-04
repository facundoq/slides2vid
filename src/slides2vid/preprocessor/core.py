

from abc import abstractmethod
from pathlib import Path
from slides2vid.core import Project


class Preprocessor:

    @abstractmethod
    def preprocess(self)->Project:
        raise NotImplementedError
    

    def generate_images_from_pdf(self,pdf_path:Path):
        
        last_modified_pdf = pdf_path.stat().st_mtime
        image_paths = [self.image_path(i) for i in range(n)]
        images_exist = all(map(lambda p: p.exists(),image_paths))
        if last_modified_pdf != self.last_modified_pdf or not images_exist:
            images = convert_from_path(pdf_path)
            pbar = tqdm.tqdm(enumerate(images),total=n)
            pbar.set_description("Generating slide images")
            for i,image in pbar:
                image.save(self.image_path(i))
            images_changed = True
        else:
            images_changed = False

        self.last_modified_pdf = last_modified_pdf
        return image_paths,images_changed