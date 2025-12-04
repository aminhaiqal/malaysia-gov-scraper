from importlib import import_module
import yaml


CONFIG = yaml.safe_load(open('configs/settings.yaml'))

SCRAPERS = {}

for s in CONFIG.get('scrapers', []):
    module_name = s['module']
    try:
        mod = import_module(f"{module_name}")
        cls = getattr(mod, f"{s['name'].upper()}Scraper", None)
        # fallback: look for class with name pattern
        if not cls:
            for attr in dir(mod):
                obj = getattr(mod, attr)
                if hasattr(obj, 'parse_article'):
                    cls = obj
                    break
        if cls:
            SCRAPERS[s['name']] = {
                'class': cls,
                'start_urls': s.get('start_urls', []),
                'selectors': s.get('selectors', {})
            }
    except Exception as e:
        print('Failed to load', module_name, e)