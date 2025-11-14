


from pathlib import Path
from slides2vid.converter.odp import ODPAudioConverter, ODPImageConverter
from slides2vid.tts.gtts import GoogleTTS

def assert_paths_exist(paths):
    for path in paths:
        assert path.exists()

def test_odt_audio_preprocessor():
    odp_path = Path("test/data/sample1.odp")
    work_path = Path("test/work_folders/odp_audio")
    work_path.mkdir(parents=True, exist_ok=True)
    engine = GoogleTTS("en")
    converter = ODPAudioConverter(work_path,odp_path,engine)
    texts = converter.get_slides_text()
    assert isinstance(texts,dict)
    paths,changed = converter.run()
    assert len(paths) == len(changed)
    assert len(paths) == len(texts)
    assert_paths_exist(paths)


def test_odt_image_preprocessor():
    odp_path = Path("test/data/sample1.odp")
    work_path = Path("test/work_folders/odp_image")
    work_path.mkdir(parents=True, exist_ok=True)
    preprocessor = ODPImageConverter(work_path,odp_path)
    paths,changed = preprocessor.run()
    assert_paths_exist(paths)
    assert len(paths) == len(changed)