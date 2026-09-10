from textual.app import App, ComposeResult
from textual.containers import Container
from textual.binding import Binding
from textual.widgets import Static

from stations.radiobrowser import search_lofi
from player.mpv import Player


class CofiiApp(App):
    CSS = """
    Screen {
        align: center middle;
    }

    #panel {
        width: 56;
        height: auto;
        border: round #c4a574;
        padding: 1 2;
        color: #e8e0d5;
    }

    #panel .hint {
        color: #8a7f72;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit", show=False),
        Binding("up", "prev_station", "Prev", show=False),
        Binding("down", "next_station", "Next", show=False),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.player = Player()
        self.stations = search_lofi(10)
        self.index = 0

    def compose(self) -> ComposeResult:
        with Container(id="panel"):
            yield Static("", id="status")
            yield Static("↑↓ change station · q quit", classes="hint")

    def on_mount(self) -> None:
        if self.stations:
            self._play_index(0)

    def action_prev_station(self) -> None:
        if not self.stations:
            return
        self._play_index((self.index - 1) % len(self.stations))

    def action_next_station(self) -> None:
        if not self.stations:
            return
        self._play_index((self.index + 1) % len(self.stations))

    def _play_index(self, i: int) -> None:
        if not (0 <= i < len(self.stations)):
            return
        self.index = i
        station = self.stations[i]
        self.player.play(station["url_resolved"])
        n = i + 1
        total = len(self.stations)
        self.query_one("#status", Static).update(
            f"Playing: {station['name']}\n[{n}/{total}]"
        )

    def on_unmount(self) -> None:
        self.player.stop()


def main() -> None:
    CofiiApp().run()


if __name__ == "__main__":
    main()
