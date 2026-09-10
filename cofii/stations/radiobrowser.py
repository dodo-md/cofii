import httpx

BASE = "https://de1.api.radio-browser.info"
HEADERS = {"User-Agent": "cofii/0.1.0"}


def search_lofi(limit: int = 20, offset: int = 0) -> list[dict]:
    r = httpx.get(
        f"{BASE}/json/stations/search",
        params={
            "tag": "lofi",
            "limit": limit,
            "offset": offset,
            "hidebroken": "true",
            "order": "clickcount",
            "reverse": "true",
        },
        headers=HEADERS,
        timeout=15,
    )
    r.raise_for_status()
    return r.json()
