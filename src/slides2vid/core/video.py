from pathlib import Path
import subprocess
from ..utils import tool
import ffmpeg




class SlideGenerator:
    def __init__(self, work_folder,verbose=False):
        self.work_folder = work_folder
        self.verbose=verbose

    def generate(self, image_path: Path, audio_path: Path, video_path: Path):
        raise NotImplementedError(f"{self.__class__.__name__} must implement the generate method")

    def concatenate(self, video_files: list[Path], out_path: Path) -> None:
        raise NotImplementedError(f"{self.__class__.__name__} must implement the concatenate method")
    


class FFMPEGVideoSlideGenerator(SlideGenerator):
    def __init__(self, work_folder, verbose=False):
        super().__init__(work_folder, verbose)
        tool.check_ffmpeg_installed()

    def generate(self, image_path: Path, audio_path: Path, video_path: Path) -> None:
        stream = ffmpeg.input(str(image_path), loop=1).filter('crop', 'iw-mod(iw,2)', 'ih-mod(ih,2)')
        audio = ffmpeg.input(str(audio_path))
        options = {
            "acodec": "aac",
            "b:a": "192k",
            "vcodec": "libx264",
            "pix_fmt": "yuv420p",
            "tune":"stillimage",
        }
        loglevel = "quiet" if self.verbose else "error"
        out,err = ffmpeg.output(stream,audio,str(video_path), shortest=None, loglevel=loglevel,**options).run(overwrite_output=True)
        if err is not None:
            raise tool.ToolError(err.decode('utf-8'))
        
        
    def concatenate(self, video_files: list[Path], out_path: Path) -> None:
        loglevel = "quiet" if self.verbose else "error"
        filelist = self.work_folder/'filelist'
        with open(filelist, 'w') as f:
            for video_file in video_files:
                f.write(f'file {video_file.absolute()}\n')
        (
            ffmpeg
            .input(filelist, format='concat', safe=0)
            .output(str(out_path), c='copy',loglevel=loglevel)
            .run(overwrite_output=True)
        )