import requests
from time import sleep
from random import uniform
from typing import Optional


DEFAULT_HEADERS = {"User-Agent": "gov-scraper-bot/1.0 (+https://example.com)"}

def fetch(url: str, headers: Optional[dict] = None, timeout: int = 20) -> str:
    h = DEFAULT_HEADERS.copy()
    if headers:
        h.update(headers)
        for attempt in range(3):
            try:
                r = requests.get(url, headers=h, timeout=timeout)
                r.raise_for_status()
                return r.text
            except Exception:
                sleep(1 + uniform(0, 1))
                raise RuntimeError(f"Failed to fetch {url}")