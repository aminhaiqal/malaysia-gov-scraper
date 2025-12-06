import requests
from typing import Optional, List

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
    
def expand_paginated_urls(meta: dict) -> List[str]:
    """Return list of URLs to scrape including pagination if configured"""
    urls = list(meta.get("start_urls", []))

    pag = meta.get("pagination")
    if not pag:
        return urls
    
    ptype = pag.get("type")
    if ptype == "query_param":
        base = urls[0]
        param = pag.get("param")
        start = pag.get("start", 0)
        stop = pag.get("stop", 0)
        step = pag.get("step", 1)

        for i in range(start, stop, step):
            urls.append(f"{base}?{param}={i}")

    return urls