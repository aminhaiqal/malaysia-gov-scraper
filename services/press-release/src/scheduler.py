import concurrent.futures
from .registry import SCRAPERS
from .core.http import expand_paginated_urls, fetch
from .core.publisher import QdrantPublisher
from .core.models import Article
from .core.storage import DocumentStore
from typing import List


PUBLISHER = None
STORE = None

def _ensure_publisher():
    """Initialize global publisher if not already done"""
    global PUBLISHER
    global STORE

    STORE = DocumentStore()

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
            print
            cls = meta['class']
            scraper_config = {k: v for k, v in meta.items() if k != 'class'}
            scraper = cls(config=scraper_config)

            urls_to_run = expand_paginated_urls(meta)
            print("Paginated URLs for", name, urls_to_run)

            for url in urls_to_run:
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

            if len(docs) >= 20:
                new_docs = STORE.save_articles(docs)
                if embed and new_docs:
                    PUBLISHER.publish(docs)
                docs.clear()

        except Exception as e:
            print("Article error:", link, e)

    if docs:
        new_docs = STORE.save_articles(docs)
        if embed and new_docs:
            PUBLISHER.publish(new_docs)
        docs.clear()

    return docs