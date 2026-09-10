from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, OptionList, Static
from textual.widgets.option_list import Option

from stations.radiobrowser import search_lofi
from player.mpv import Player

class CofiiApp(App):
    CSS = """
    #stations { width: 42; border: solid green; }
    #now { border: solid green; }
    """

    BINDINGS = [("q", "quit", "Quit")]

    def __init__(self):
        super().__init__()
        self.player = Player()
        self.stations = search_lofi(10)

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            yield OptionList(id="stations")
            with Vertical(id="now"):
                yield Static("cofii", id="title")
                yield Static("—", id="current")
        yield Footer()

    def on_mount(self) -> None:
        ol = self.query_one("#stations", OptionList)
        for s in self.stations:
            ol.add_option(Option(s["name"]))
        ol.focus()
        self._play_index(0)

    def on_option_list_option_highlighted(self, event: OptionList.OptionHighlighted) -> None:
        # ok tuşuyla gezerken burası tetiklenir
        self._play_index(event.option_index)

    def _play_index(self, i: int) -> None:
        if not (0 <= i < len(self.stations)):
            return
        s = self.stations[i]
        self.player.play(s["url_resolved"])
        self.query_one("#current", Static).update(s["name"])

    def on_unmount(self) -> None:
        self.player.stop()

def main():
    CofiiApp().run()

if __name__ == "__main__":
    main()