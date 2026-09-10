from stations.radiobrowser import search_lofi
from player.mpv import Player

def main():
    stations = search_lofi(10)
    for i, s in enumerate(stations, 1):
        print(f"{i}. {s['name']}")

    choice = int(input("Seç: ")) - 1
    url = stations[choice]["url_resolved"]

    player = Player()
    player.play(url)
    input("Çalıyor… durdurmak için Enter")
    player.stop()

if __name__ == "__main__":
    main()