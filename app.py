from stations.radiobrowser import search_lofi
from player.mpv import Player

def main():
    stations = search_lofi(10)
    for i, s in enumerate(stations, 1):
        print(f"{i}. {s['name']}")

    choice = int(input("\nselect a radio: ")) - 1
    url = stations[choice]["url_resolved"]

    player = Player()
    player.play(url)
    input("playing... press Enter to stop")
    player.stop()

if __name__ == "__main__":
    main()