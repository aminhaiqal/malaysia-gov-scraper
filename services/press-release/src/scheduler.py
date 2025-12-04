import concurrent.futures
from registry import SCRAPERS
from core.http import fetch
from core.cleaners import clean_text
from core.models import Document
from core.publisher import QdrantPublisher
from core.pdf import extract_pdf_text_from_url
import uuid


PUBLISHER = None


def _ensure_publisher():
    global PUBLISHER
    if PUBLISHER is None:
        import yaml
        cfg = yaml.safe_load(open('config/settings.yaml'))
        q = cfg.get('qdrant', {})
        PUBLISHER = QdrantPublisher(url=q.get('url'))

def run_all():
    _ensure_publisher()
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
        futures = []
        for name, meta in SCRAPERS.items():
            cls = meta['class']
            scraper = cls(config={})
            for url in meta.get('start_urls', []):
                futures.append(ex.submit(run_scraper, scraper, url))
        for f in concurrent.futures.as_completed(futures):
            try:
                f.result()
            except Exception as e:
                print('error', e)

def run_scraper(scraper, index_url: str):
    html = fetch(index_url)
    links = scraper.list_links(html)
    for link in links:
        try:
            raw = fetch(link) if not link.lower().endswith('.pdf') else None
            if link.lower().endswith('.pdf'):
                text = extract_pdf_text_from_url(link)
                source = 'PDF'
            else:
                text = scraper.parse_article(raw)['text']
                source = 'HTML'
            text = clean_text(text)
            doc = Document(
                id=str(uuid.uuid4()),
                title=scraper.parse_article(raw).get('title'),
                ministry=scraper.name.upper(),
                date=scraper.parse_article(raw).get('date'),
                source=source,
                url=link,
                text=text,
                metadata={}
            )
            # Embedding placeholder: use your embedding function
            embedding = [0.0] * 1536
            PUBLISHER.publish(doc.id, doc.text, doc.dict(), embedding)
        except Exception as e:
            print('article error', link, e)