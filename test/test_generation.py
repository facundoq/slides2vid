from pathlib import Path
import shutil
import pytest
from slides2vid.core import make_video

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
    make_video(text,images,video,work_path=work_path)
    assert video.exists()