import subprocess


FFMPEG_NAME = "ffmpeg"
FFMPEG_CHECK_ARGS = [FFMPEG_NAME, "-version"]

SOFFICE_NAME = "soffice"
SOFFICE_CHECK_ARGS = [SOFFICE_NAME, "--version"]

def executable_installed(executable_args: list[str]) -> bool:
    try:
        subprocess.run(executable_args, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False
    
def check_soffice_installed():
    if not executable_installed(SOFFICE_CHECK_ARGS):
        raise ToolNotInstalled(SOFFICE_NAME)
    
def check_ffmpeg_installed():
    if not executable_installed(FFMPEG_CHECK_ARGS):
        raise ToolNotInstalled(FFMPEG_NAME)

def soffice(args: list[str]):
    args = [SOFFICE_NAME, "--headless"] + args
    subprocess.check_call
    try:
        subprocess.run(args, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        raise ToolError(f"Error while running {SOFFICE_NAME}: {e.stderr.decode('utf-8')}")

class Slides2VidError(Exception):
    pass

class ToolNotInstalled(Slides2VidError):
    def __init__(self, name: str, *args: object) -> None:
        super().__init__(*args)
        self.name=name
        self.message=f"Executable {name} is not installed. Please install it through your system package manager (e.g. apt in ubuntu) before using project configuration."

    def __str__(self) -> str:
        return self.message

class ToolError(Slides2VidError):
    def __init__(self, message: str, *args: object) -> None:
        super().__init__(*args)
        self.message=message

    def __str__(self) -> str:
        return self.message
