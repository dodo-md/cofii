import shutil
import subprocess


class Player:
    def __init__(self) -> None:
        self._proc: subprocess.Popen | None = None
        self._url: str | None = None
        self.paused: bool = False

    @property
    def playing(self) -> bool:
        return self._proc is not None and self._proc.poll() is None and not self.paused

    def play(self, url: str) -> None:
        if shutil.which("mpv") is None:
            raise RuntimeError(
                "mpv not found. Install it first (e.g. brew install mpv)."
            )
        self._kill()
        self._url = url
        self.paused = False
        self._proc = subprocess.Popen(
            ["mpv", "--no-video", "--really-quiet", url],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    def stop(self) -> None:
        self._kill()
        self.paused = False
        self._url = None

    def pause(self) -> None:
        if not self.playing:
            return
        self._kill()
        self.paused = True

    def resume(self) -> None:
        if not self.paused or not self._url:
            return
        self.play(self._url)

    def toggle(self) -> None:
        if self.paused:
            self.resume()
        else:
            self.pause()

    def _kill(self) -> None:
        if self._proc and self._proc.poll() is None:
            self._proc.terminate()
            try:
                self._proc.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self._proc.kill()
        self._proc = None
