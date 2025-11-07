#!/usr/bin/env python
import faulthandler

from slides2vid.core import Project
from slides2vid.preprocessor.pdf import PDFImageConverter
from slides2vid.preprocessor.pptx import PPTXAudioConverter
from slides2vid.tts.chatterbox import ChatterboxTTS
from slides2vid.tts.gtts import GoogleTTS
faulthandler.enable()
# from pptx import Presentation
import lxml.etree
#import pptx

# from slides2vid.core import make_video

from pathlib import Path
import tempfile
import argparse
import os




def main():
    parser = argparse.ArgumentParser(description='PPT Presenter help.')
    parser.add_argument('-a --pptx', help='input pptx path', required=True)
    parser.add_argument('-v --pdf', help='input pdf path', required=True)
    parser.add_argument('-o', '--output', help='output path', required=True)
    parser.add_argument('-l', '--language', help='Language code: en, es, etc..', required=True)
    parser.add_argument('-t', '--tts',  choices=['gtts', 'chatterbox'], help='TTS engine to generate audio', default="chatterbox")
    args = parser.parse_args()
    print("Starting..")
    with tempfile.TemporaryDirectory() as work_path:
        work_path = Path("output")
        work_path.mkdir(parents=True, exist_ok=True)
        p = Project(work_path)
        images = PDFImageConverter(args.pdf,work_path)
        
        if args.tts == "gtts":
            tts_engine = GoogleTTS(args.language)
        elif args.tts == "chatterbox":
            tts_engine = ChatterboxTTS(args.language)
        else:
            raise ValueError(f"Unknown tts engine: {args.tts}")
        audios = PPTXAudioConverter(args.pptx,work_path,tts_engine)
        p.run(images,audios,args.output)


if __name__ == '__main__':
    main()