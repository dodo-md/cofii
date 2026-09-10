import shutil
import subprocess


class Player:
    def __init__(self) -> None:
        self._proc: subprocess.Popen | None = None

    def play(self, url: str) -> None:
        if shutil.which("mpv") is None:
            raise RuntimeError(
                "mpv not found. Install it first (e.g. brew install mpv)."
            )
        self.stop()
        self._proc = subprocess.Popen(
            ["mpv", "--no-video", "--really-quiet", url],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    def stop(self) -> None:
        if self._proc and self._proc.poll() is None:
            self._proc.terminate()
            try:
                self._proc.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self._proc.kill()
        self._proc = None
