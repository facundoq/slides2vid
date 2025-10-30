from pathlib import Path
import pytest
from slides2vid.main import make_video

def test_generation():
    filename = "sample1"
    folder_path = Path("data")
    make_video(folder_path/f"{filename}.pptx",folder_path/f"{filename}.pdf",folder_path/f"{filename}.mp4",work_path=Path(f"test/temp/{filename}"))