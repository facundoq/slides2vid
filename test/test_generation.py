from pathlib import Path
import shutil
import pytest
from slides2vid.core import Project

import logging
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

def test_generation(tmp_path):
    filename = "sample2"
    folder_path = Path("data")
    text = folder_path/f"{filename}.pptx"
    images = folder_path/f"{filename}.pdf"
    video = folder_path/f"{filename}.mp4"
    video.unlink(missing_ok=True)   
    work_path = Path(f"test/temp/{filename}")
    # work
    #shutil.rmtree(work_path)
    #work_path.mkdir(parents=True, exist_ok=True)
    p = Project(work_path,language="en")
    p.make_video(text,images,video)
    assert video.exists()