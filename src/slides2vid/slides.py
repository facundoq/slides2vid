from pathlib import Path
from subprocess import run

import ffmpeg


class SlideGenerator:
    def __init__(self, work_folder):
        self.work_folder = work_folder

    def generate(self, image_path: Path, audio_path: Path, video_path: Path):
        raise NotImplementedError("Slide generator must implement generate method")


FFMPEG_NAME = "ffmpeg"


class FFMPEGSlideGenerator(SlideGenerator):
    def generate(self, image_path: Path, audio_path: Path, video_path: Path) -> None:
        stream = ffmpeg.input(str(image_path), loop=1).filter('crop', 'iw-2*mod(iw,2)', 'ih-2*mod(ih,2)')
        audio = ffmpeg.input(str(audio_path))
        options = {
            "acodec": "aac",
            "b:a": "192k",
            "vcodec": "libx264",
            "pix_fmt": "yuv420p",
            "tune":"stillimage",
            
        }

        out = ffmpeg.output(stream,audio,str(video_path), shortest=None, loglevel="quiet",**options).run(overwrite_output=True)
        # command_base = ffmpeg.input(str(image_path), loop=1)
        # .video_filter('crop', 'iw-2*mod(iw,2)', 'ih-2*mod(ih,2)')
        # .output(str(self.output_folder / 'slide.mp4'), vcodec='libx264', tune='stillimage', acodec='aac', b:a='192k', pix_fmt='yuv420p')

        # command = command_base.run_async()

        # out = run(command)
        #assert out.returncode == 0, f"Slide generation failed"
