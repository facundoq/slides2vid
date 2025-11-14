from returns.result import Result, Failure, Success

import gtts
import gtts.lang
from slides2vid.converter import Converter
from slides2vid.converter.folder import FolderConverter
from slides2vid.converter.odp import ODPAudioConverter, ODPImageConverter
from slides2vid.converter.pdf import PDFImageConverter
from slides2vid.converter.pptx import PPTXAudioConverter
from slides2vid.core.project import Project
from slides2vid.core.video import SlideGenerator
from slides2vid.tts.base import TTSEngine
from slides2vid.tts.chatterbox import ChatterboxTTS,CHATTERBOX_LANGUAGES
from slides2vid.tts.gtts import GoogleTTS
from pathlib import Path
import argparse




class ProjectFactory:

    audio_input_extensions = ["pptx","odt"]
    image_input_extensions = ["pptx","odp","pdf"]


    image_folder_extensions = ["png","jpg","jpeg","gif","tiff"]
    audio_folder_extensions = ["mp3","m4a","aac","wav"]

    def __init__(self,work_path:Path) -> None:
        super().__init__()
        self.work_path = work_path

    def get_tts_engine(self,tts:str,args:dict)->Result[TTSEngine,str]:
        tts_engine = None
        language = args["language"]
        if tts == "gtts":
            if not language in gtts.lang.tts_langs():
                return Failure(f"Language not supported by gtts: {language}")
            tts_engine = GoogleTTS(language)
        elif tts == "chatterbox":
            if not language in CHATTERBOX_LANGUAGES.keys():
                return Failure(f"Language not supported by chatterbox: {language}")
            tts_engine = ChatterboxTTS(language)
        else:
            return Failure(f"Unknown tts engine: {tts}")

        return Success(tts_engine)

    
    def get_audio_converter(self,path:Path,tts_engine:TTSEngine,verbose:bool)->Result[Converter,str]:
        if not path.exists():
            return Failure(f"Audio file does not exist: {path}")
        
        if path.is_dir():
            converter = FolderConverter(self.work_path, path, self.audio_folder_extensions, verbose=verbose)
            return Success(converter)
        else:
            if not path.suffix in self.audio_input_extensions:
                return Failure(f"Unknown audio format: {path.suffix}")
        if path.suffix == ".pptx":
            return Success(PPTXAudioConverter(self.work_path,path,tts_engine,verbose=verbose))
        elif path.suffix == ".odp":
            return Success(ODPAudioConverter(self.work_path,path,tts_engine,verbose=verbose))
        else:
            return Failure(f"Unknown audio format: {path}")


    def get_image_converter(self,path:Path,verbose:bool)->Result[Converter,str]:
        
        if not path.exists():
            return Failure(f"Input file does not exist: {path}")
        
        if path.is_dir():
            converter = FolderConverter(self.work_path, path, self.audio_folder_extensions, verbose=verbose)
            return Success(converter)
        else:
            if not path.suffix in self.audio_input_extensions:
                return Failure(f"Unknown input format: {path}")
        if path.suffix == ".pdf":
            return Success(PDFImageConverter(self.work_path,path,verbose=verbose))
        elif path.suffix == ".odp":
            return Success(ODPImageConverter(self.work_path,path,verbose=verbose))
        else:
            return Failure(f"Unknown input format: {path}")

    def make_project(self,audio_path:Path,image_path:Path,output_path:Path,tts_engine:TTSEngine,verbose:bool)->Result[Project,str]:
        audio_converter_result = self.get_audio_converter(audio_path,tts_engine,verbose)
        image_converter_result = self.get_image_converter(image_path,verbose)

        match (audio_converter_result,image_converter_result):
            case (Success(audio_converter),Success(image_converter)):
                generator =SlideGenerator(self.work_path)
                p = Project(self.work_path,generator,image_converter,audio_converter,output_path)
                return Success(p)
            case (Failure(audio_error),Success(image_converter)):
                return Failure(f"Audio input error: {audio_error}")
            case (Success(audio_converter),Failure(image_error)):
                return Failure(f"Image input error: {image_error}")
            case (Failure(audio_error),Failure(image_error)):
                return Failure(f"Audio input error: {audio_error}\n and\n Image input error: {image_error}")
            case _:
                return Failure("Unknown error")
            