import os
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container
from textual.widgets import Static

from cofii.player.mpv import Player
from cofii.stations.radiobrowser import search_lofi


class CofiiApp(App):
    CSS = """
    Screen {
        align: center middle;
    }

    #panel {
        width: 56;
        height: auto;
        border: round #c4a574;
        border-title-align: center;
        border-title-color: #c4a574;
        padding: 1 2;
        color: #e8e0d5;
    }

    #panel .hint {
        color: #8a7f72;
    }
    """

    BINDINGS = [
        Binding("p", "toggle_pause", "Pause", show=False),
        Binding("q", "quit", "Quit", show=False),
        Binding("up", "prev_station", "Prev", show=False),
        Binding("down", "next_station", "Next", show=False),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.player = Player()
        self.page_size = 10
        self.offset = 0
        self.stations = search_lofi(self.page_size, offset=0)
        self.index = 0
        self.loading = False

    def compose(self) -> ComposeResult:
        with Container(id="panel") as panel:
            panel.border_title = "cofii"
            yield Static("", id="status")
            yield Static("↑↓ change station · p pause · q quit", classes="hint")

    def on_mount(self) -> None:
        if self.stations:
            self._play_index(0)

    def action_toggle_pause(self) -> None:
        if not self.stations:
            return
        self.player.toggle()
        self._update_status()

    def action_prev_station(self) -> None:
        if not self.stations:
            return
        if self.index > 0:
            self._play_index(self.index - 1)
            return
        if self.offset == 0:
            return
        if not self._load_page(self.offset - self.page_size):
            return
        self._play_index(len(self.stations) - 1)


    def action_next_station(self) -> None:
        if not self.stations:
            return
        if self.index < len(self.stations) - 1:
            self._play_index(self.index + 1)
            return
        if not self._load_page(self.offset + self.page_size):
            return
        self._play_index(0)

    def _load_page(self, offset: int) -> bool:
        if self.loading:
            return False
        self.loading = True
        try:
            batch = search_lofi(self.page_size, offset=offset)
        finally:
            self.loading = False

        if not batch:
            return False

        self.stations = batch
        self.offset = offset
        return True

    def _play_index(self, i: int) -> None:
        if not (0 <= i < len(self.stations)):
            return
        self.index = i
        station = self.stations[i]
        self.player.play(station["url_resolved"])
        self._update_status()

    def _update_status(self) -> None:
        if not self.stations:
            return
        name = self.stations[self.index]["name"]
        prefix = "paused" if self.player.paused else "playing"
        self.query_one("#status", Static).update(f"{prefix}: {name}")

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def on_unmount(self) -> None:
        self.clear_terminal()
        self.player.stop()


def main() -> None:
    CofiiApp().run()


if __name__ == "__main__":
    main()
