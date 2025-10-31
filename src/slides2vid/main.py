#!/usr/bin/env python
import faulthandler

from slides2vid.core import make_video
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
    args = parser.parse_args()
    print("Starting..")
    with tempfile.TemporaryDirectory() as work_path:
        work_path = Path("output")
        os.makedirs(work_path, exist_ok=True)
        make_video(Path(args.pptx), Path(args.pdf), Path(args.output),work_path)


if __name__ == '__main__':
    main()