import requests
from typing import Optional
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse


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
    
def expand_paginated_urls(meta):
    start_urls = meta.get("start_urls", [])
    pagination = meta.get("pagination")

    urls = []

    for base_url in start_urls:
        if base_url.lower().endswith(".pdf"):
            urls.append(base_url)
            continue
        urls.append(base_url)

        if pagination and pagination.get("type") == "query_param":
            param = pagination.get("param")
            start = pagination.get("start")
            stop = pagination.get("stop")
            step = pagination.get("step", 1)

            parsed = urlparse(base_url)
            qs = parse_qs(parsed.query)
            existing_page = int(qs.get(param, [None])[0]) if param in qs else None

            for i in range(start, stop + 1, step):
                if existing_page is not None and i == existing_page:
                    continue

                qs[param] = [str(i)]
                new_query = urlencode(qs, doseq=True)
                new_url = urlunparse((
                    parsed.scheme,
                    parsed.netloc,
                    parsed.path,
                    parsed.params,
                    new_query,
                    parsed.fragment
                ))
                urls.append(new_url)

    return urls
