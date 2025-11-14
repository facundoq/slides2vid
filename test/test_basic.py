
from pathlib import Path

import pytest

from slides2vid.converter.odp import ODPAudioConverter, ODPImageConverter
from slides2vid.core.project import Project
from slides2vid.core.video import FFMPEGVideoSlideGenerator
from slides2vid.tts.chatterbox import ChatterboxTTS
from slides2vid.tts.gtts import GoogleTTS


def assert_paths_exist(paths):
    for path in paths:
        assert path.exists()

@pytest.fixture
def tts_engine():
    return GoogleTTS("en")

@pytest.mark.parametrize("engine", [GoogleTTS("en"),
                                    ChatterboxTTS("en","cpu"),
                                    ChatterboxTTS("en","cpu",audio_prompt_path=Path("test/data/en/voice_models/henry5.wav"))
])
def test_odp_ffmpeg_gtts(engine):
    filename = f"sample2"
    odp_path = Path(f"test/data/en/{filename}.odp")
    work_path = Path(f"test/work_folders/basic/{engine}/{filename}/")
    work_path.mkdir(parents=True, exist_ok=True)
    audio_converter = ODPAudioConverter(work_path,odp_path,engine,verbose=True)
    image_converter = ODPImageConverter(work_path,odp_path,verbose=True)
    generator = FFMPEGVideoSlideGenerator(work_path,verbose=True)
    output_path= work_path/"output.mp4"
    p = Project(work_path,generator,image_converter,audio_converter,output_path,verbose=True)
    p.run()
    assert output_path.exists()
