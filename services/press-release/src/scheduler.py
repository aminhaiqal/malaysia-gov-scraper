import concurrent.futures
import uuid
from .registry import SCRAPERS
from .core.http import fetch
from .core.models import Document
from .core.publisher import QdrantPublisher
from .core.pdf import extract_pdf_text_from_url
from .core.utils import stable_id
from .embeddings.embedder import embed_text
from .embeddings.chunking import chunk_text

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
                futures.append(ex.submit(run_scraper, scraper, url))

        for f in concurrent.futures.as_completed(futures):
            try:
                f.result()
            except Exception as e:
                print('Scraper error:', e)
    
    if PUBLISHER:
        PUBLISHER.trigger_indexing()

def run_scraper(scraper, index_url: str):
    """Run a single scraper and publish chunks to Qdrant"""
    html = fetch(index_url)
    links = scraper.list_links(html)
    seen = set()

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
                text = extract_pdf_text_from_url(link)
                title, date = None, None
                source = "PDF"
                category = ""
            else:
                raw = fetch(link)
                article_data = scraper.parse_article(raw)
                text = article_data.get("text", "")
                title = article_data.get("title", "")
                date = article_data.get("date")
                category = article_data.get("category", "")
                source = "HTML"

            if not text or len(text.strip()) == 0:
                continue  # skip empty articles

            base_id = stable_id(link)

            # Create Document object
            doc = Document(
                id=base_id,
                title=title,
                ministry=scraper.name.upper(),
                date=date,
                source=source,
                url=link,
                text=text,
                metadata={
                    "title": title,
                    "date": date,
                    "category": category,
                    "pdfs": article_data.get("pdfs", []) if source == "HTML" else [],
                },
            )

            # Split text into chunks
            for idx, chunk in enumerate(chunk_text(text, size=512), start=1):
                if not chunk.strip():
                    continue  # skip empty chunks

                chunk_id = str(uuid.uuid4())
                enriched_text = (
                    f"Title: {title}\n"
                    f"Ministry: {scraper.name.upper()}\n"
                    f"Date: {date}\n"
                    f"Category: {category}\n"
                    f"Text: {chunk}"
                )

                # Embed and normalize
                embedding = embed_text(enriched_text)
                if isinstance(embedding[0], list):
                    embedding = embedding[0]  # flatten if nested

                # Publish chunk to Qdrant
                PUBLISHER.publish(
                    doc_id=chunk_id,
                    text=chunk,
                    metadata={**doc.metadata, "chunk_index": idx},
                    embedding=embedding
                )

        except Exception as e:
            print("Article error:", link, e)
