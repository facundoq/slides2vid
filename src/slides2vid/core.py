import faulthandler

import tqdm

from slides2vid.video import VideoConcatenator
faulthandler.enable()

from pathlib import Path

from subprocess import run

from pdf2image import convert_from_path
from pptx import Presentation
from gtts import gTTS
from slides2vid.slides import FFMPEGSlideGenerator, SlideGenerator

FFMPEG_NAME = 'ffmpeg'


def make_video(pptx_path:Path, pdf_path:Path, output_path:Path,work_path:Path):
    generator = FFMPEGSlideGenerator(work_path)
    
    images_from_path = convert_from_path(pdf_path)
    prs = Presentation(str(pptx_path))
    assert len(images_from_path) == len(prs.slides)
    video_list = []
    iterable = enumerate(zip(prs.slides, images_from_path))
    pbar = tqdm.tqdm(iterable,total=len(prs.slides),desc="Generating slide videos")
    for i, (slide, image) in pbar:
        if slide.has_notes_slide:
            notes = slide.notes_slide.notes_text_frame.text
            image_path = work_path / f'frame_{i}.jpg'
            audio_path = work_path / f'frame_{i}.mp3'
            video_path = work_path / f'frame_{i}.mp4'
            # image.save(image_path)
            # tts = gTTS(text=notes, lang='en')
            # tts.save(audio_path)
            # generator.generate(image_path, audio_path,video_path)
            video_list.append(video_path)
        else:
            print(f"Slide {i} has no text notes, skipping.")
    concatenator = VideoConcatenator(work_path)
    concatenator.concatenate(video_list,output_path)
    # video_list_str = 'concat:' + '|'.join(map(str,video_list))
    # print("Concatenating slide videos...",end="")
    # ffmpeg_concat(video_list_str, output_path)
    print(" done.")

def ffmpeg_concat(video_list_str, out_path):
    
    out =  run([FFMPEG_NAME, '-y', '-f', 'mpegts', '-i', '{}'.format(video_list_str), '-c', 'copy', '-bsf:a', 'aac_adtstoasc', out_path])
    assert out.returncode == 0, f"Slide video concatenation failed"