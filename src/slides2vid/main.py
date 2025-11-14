#!/usr/bin/env python
import sys
import tempfile
import argparse
from pathlib import Path
from returns.result import Result, Failure, Success

from .utils.tool import Slides2VidError

from .core.factory import ProjectFactory


audio_help = f'input to extract audio, file formats: {",".join(ProjectFactory.audio_input_extensions)}; alternatively, a folder with audio files can be provided.'

image_help = f"input to extract images, file formats: {','.join(ProjectFactory.image_input_extensions)}; alternatively, a folder with image files can be provided."

def main():
    parser = argparse.ArgumentParser(description='PPT Presenter help.')
    parser.add_argument('-a --audio', type=Path, help=audio_help, required=True)
    parser.add_argument('-i --image', type=Path, help='input pdf path', required=True)
    parser.add_argument('-o', '--output', type=Path, help='output path', required=True)
    parser.add_argument('-l', '--language', help='Language for tts. Use ISO 639-1 codes: en, es, etc. Note that not all tts engines support all languages.', required=True)
    parser.add_argument('-t', '--tts',  choices=['gtts', 'chatterbox'], help='TTS engine to generate audio', default="chatterbox")
    parser.add_argument('-w', '--workfolder',  type=Path, help='Folder used to generate intermediate files and store caches to speedup subsequent runs.', default=None)
    parser.add_argument('-d', '--device',  type=Path, help='Device used to run chatterbox (if selected).', choices =["cpu","cuda"], default="cpu")
    parser.add_argument('-v', '--verbose', help='Verbose mode', action='store_true')

    args = parser.parse_args()

    if args.verbose:
        print("Starting..")
    if args.workfolder is None:
        work_path = Path(tempfile.mkdtemp())
    else:
        work_path = args.workfolder
        work_path.mkdir(parents=True, exist_ok=True)
    factory = ProjectFactory(work_path)

    tts_engine_result = factory.get_tts_engine(args.tts,vars(args))

    do_make_project = lambda tts_engine: factory.make_project(args.audio,args.image,args.output,tts_engine,args.verbose)
    match tts_engine_result.bind(do_make_project):
        case Failure(e):
            print(e,file=sys.stderr)
            sys.exit(1)
        case Success(p):
            try:
                p.run()
            except Slides2VidError as e:
                print(e,file=sys.stderr)
                sys.exit(1)
        


if __name__ == '__main__':
    main()