import subprocess

class Player:
    def __init__(self):
        self._proc: subprocess.Popen | None = None

    def play(self, url: str) -> None:
        self.stop()
        self._proc = subprocess.Popen(
            ["mpv", "--no-video", "--really-quiet", url],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    def stop(self) -> None:
        if self._proc and self._proc.poll() is None:
            self._proc.terminate()
            self._proc.wait(timeout=3)
        self._proc = None