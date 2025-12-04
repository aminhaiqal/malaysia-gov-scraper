import requests
from typing import Optional

def fetch(url: str, timeout: int = 20) -> Optional[str]:
    """
    Fetch HTML using a normal HTTP request (no JS).
    Includes realistic browser headers for reliability.
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/142.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Connection": "keep-alive",
    }

    try:
        res = requests.get(url, headers=headers, timeout=timeout)
        if res.status_code >= 400:
            print(f"[Warning] HTTP {res.status_code} for {url}")
        return res.text
    except Exception as e:
        print(f"[Error] Failed to fetch {url}: {e}")
        return None
