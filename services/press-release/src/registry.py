from importlib import import_module
import yaml

CONFIG = yaml.safe_load(open('configs/settings.yaml'))

SCRAPERS = {}

for s in CONFIG.get('scrapers', []):
    module_name = s['module']
    try:
        mod = import_module(f"{module_name}")

        cls_name = s.get('class')
        if cls_name:
            cls = getattr(mod, cls_name, None)
        else:
            cls = getattr(mod, f"{s['name'].replace('-', '').title()}Scraper", None)

        if cls:
            SCRAPERS[s['name']] = {
                'class': cls,
                'start_urls': s.get('start_urls', []),
                'selectors': s.get('selectors', {}),
                'pagination': s.get('pagination', None)
            }
        else:
            print(f"No scraper class found for {s['name']} in {module_name}")

    except Exception as e:
        print('Failed to load', module_name, e)
