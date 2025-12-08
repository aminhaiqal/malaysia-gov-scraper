import concurrent.futures
from .registry import SCRAPERS
from .core.http import expand_paginated_urls, fetch
from .core.publisher import QdrantPublisher
from .core.models import Article
from .core.storage import DocumentStore
from .core.pdf_processor import PDFProcessor
from .scrapers.strategies.factory import ScrapeStrategyFactory
from typing import List


PUBLISHER = None
STORE = None

def _ensure_publisher():
    """Initialize global publisher if not already done"""
    global PUBLISHER
    global STORE
    global PROCESSOR

    STORE = DocumentStore()
    PROCESSOR = PDFProcessor()

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

def run_scraper(scraper, index_url: str, embed: bool = True, save: bool = False) -> List[Article]:
    """
    Run a scraper on a given index URL, extract articles, and optionally save or embed them.

    Args:
        scraper: HTML scraper object with `get_article(raw_html, url)` method.
        index_url: The starting page or PDF URL to scrape.
        embed: Whether to embed articles to Qdrant.
        save: Whether to save articles to the database.

    Returns:
        List[Article]: All scraped articles.
    """

    buffer: List[Article] = []
    published_count = 0
    stored_count = 0

    def process_batch(batch: List[Article]):
        """Save and/or publish a batch of articles."""
        nonlocal published_count, stored_count
        if not batch:
            return

        if save:
            new_docs = STORE.save_articles(batch)
            stored_count += len(new_docs)
            if embed and new_docs:
                PUBLISHER.publish(new_docs)
                published_count += len(new_docs)
        else:
            if embed:
                PUBLISHER.publish(batch)
                published_count += len(batch)

        batch.clear()

    if index_url.lower().endswith(".pdf"):
        strategy = ScrapeStrategyFactory.get_strategy(index_url, scraper)
        try:
            article = strategy.process(index_url)
            if article:
                buffer.append(article)
                process_batch(buffer)
        except Exception as e:
            print("PDF processing failed:", index_url, e)

        print(f"[Scraper] Stored: {stored_count}, Published: {published_count}")
        return buffer

    html = fetch(index_url)
    links = scraper.list_links(html)
    seen = set()

    for link in links:
        if link in seen:
            continue
        seen.add(link)

        # Skip index/anchor links
        if link.endswith("#") or link.rstrip("/").endswith(("press-release", "Media%20Release")):
            continue

        try:
            strategy = ScrapeStrategyFactory.get_strategy(link, scraper)
            article = strategy.process(link)
            if article:
                buffer.append(article)
                if len(buffer) >= 20:
                    process_batch(buffer)

        except Exception as e:
            print("Article error:", link, e)

    # Process remaining articles in buffer
    process_batch(buffer)
    print(f"[Scraper] Stored: {stored_count}, Published: {published_count}")
    return buffer