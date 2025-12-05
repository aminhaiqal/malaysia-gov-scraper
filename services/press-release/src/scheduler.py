import concurrent.futures
from .registry import SCRAPERS
from .core.http import fetch
from .core.publisher import QdrantPublisher
from .core.models import Article
from typing import List


PUBLISHER = None

def _ensure_publisher():
    """Initialize global publisher if not already done"""
    global PUBLISHER
    if PUBLISHER is None:
        import yaml
        cfg = yaml.safe_load(open('configs/settings.yaml'))
        q = cfg.get('qdrant', {})
        PUBLISHER = QdrantPublisher(url=q.get("url"), api_key=q.get("api_key"))

def run_all(target: str = None):
    """Run all scrapers concurrently"""
    _ensure_publisher()
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
        futures = []
        for name, meta in SCRAPERS.items():
            if target and name.lower() != target.lower():
                continue

            cls = meta['class']
            scraper_config = {k: v for k, v in meta.items() if k != 'class'}
            scraper = cls(config=scraper_config)
            for url in meta.get('start_urls', []):
                futures.append(ex.submit(run_scraper, scraper, url, True))

        for f in concurrent.futures.as_completed(futures):
            try:
                f.result()
            except Exception as e:
                print('Scraper error:', e)

def run_scraper(scraper, index_url: str, embed: bool = True) -> List[Article]:
    """Run a single scraper and publish chunks to Qdrant"""
    html = fetch(index_url)
    links = scraper.list_links(html)
    seen = set()
    docs = []

    for link in links:
        if link in seen:
            continue
        seen.add(link)

        # Skip index/anchor links
        if (link.endswith("#")
            or link.rstrip("/").endswith("press-release")
            or link.rstrip("/").endswith("siaran-media")):
            continue

        try:
            # Extract text
            if link.lower().endswith(".pdf"):
                continue

            raw = fetch(link)
            article_data = scraper.get_article(raw, link)

            docs.append(article_data)

            if embed and len(docs) >= 20:
                PUBLISHER.publish(docs)
                docs.clear()

        except Exception as e:
            print("Article error:", link, e)

    if embed and docs:
        PUBLISHER.publish(docs)
        docs.clear()

    return docs