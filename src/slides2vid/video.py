from pathlib import Path
from subprocess import run

import ffmpeg

class VideoConcatenator:
    def __init__(self, work_folder):
        self.work_folder = work_folder

    def concatenate(self, video_files: list[Path], out_path: Path) -> None:
        video_and_audio_streams = [ffmpeg.input(file) for file in video_files]

        concatenated = ffmpeg.concat(*video_and_audio_streams, v=1, a=1)
        options = {"vcodec":'libx264',
                   "acodec":'aac', 
                   "preset":'medium',
                   "tune":'stillimage',}
        out = concatenated.output(str(out_path))
        out.run(overwrite_output=True)
        