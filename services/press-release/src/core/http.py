from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from typing import Optional

def fetch(url: str, timeout: int = 20000) -> Optional[str]:
    """
    Fetch a page using Playwright and return HTML content.
    Ignores authorization errors or timeout errors, returns whatever is loaded.
    """
    html = None
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        try:
            response = page.goto(url, timeout=timeout, wait_until="load")
            if response:
                # Even if status is 401, get page content
                html = page.content()
        except PlaywrightTimeoutError:
            print(f"[Warning] Timeout loading {url}. Returning partial HTML if any.")
            html = page.content()
        except Exception as e:
            print(f"[Warning] Error loading {url}: {e}")
            try:
                html = page.content()
            except Exception:
                html = None
        finally:
            browser.close()
    return html
