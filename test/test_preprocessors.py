


from pathlib import Path
from slides2vid.preprocessor.odp import ODPAudioPreprocessor, ODPImagePreprocessor
from slides2vid.tts.gtts import GoogleTTS


def test_odt_audio_preprocessor():
    odp_path = Path("test/data/sample1.odp")
    work_path = Path("test/work_folders/odp_audio")
    work_path.mkdir(parents=True, exist_ok=True)
    engine = GoogleTTS("en")
    preprocessor = ODPAudioPreprocessor(work_path,odp_path,engine)
    texts = preprocessor.get_slides_text()
    assert isinstance(texts,dict)
    result = preprocessor.run()
    assert len(result) == len(texts)
    for i in range(len(result)):
        assert result.path(i).exists()


def test_odt_image_preprocessor():
    odp_path = Path("test/data/sample1.odp")
    work_path = Path("test/work_folders/odp_image")
    work_path.mkdir(parents=True, exist_ok=True)
    preprocessor = ODPImagePreprocessor(work_path,odp_path)
    result = preprocessor.run()
    for i in range(len(result)):
        assert result.path(i).exists()