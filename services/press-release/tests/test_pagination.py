from src.core.http import expand_paginated_urls

def test_expand_with_pagination():
    meta = {
        "start_urls": ["https://www.mof.gov.my/portal/en/archive3/press-release"],
        "pagination": {
            "type": "query_param",
            "param": "start",
            "start": 5,
            "stop": 25,
            "step": 5
        }
    }

    urls = expand_paginated_urls(meta)

    expected = [
        "https://www.mof.gov.my/portal/en/archive3/press-release",
        "https://www.mof.gov.my/portal/en/archive3/press-release?start=5",
        "https://www.mof.gov.my/portal/en/archive3/press-release?start=10",
        "https://www.mof.gov.my/portal/en/archive3/press-release?start=15",
        "https://www.mof.gov.my/portal/en/archive3/press-release?start=20",
    ]

    assert urls == expected


def test_expand_no_pagination():
    meta = {
        "start_urls": ["https://example.com"]
    }

    urls = expand_paginated_urls(meta)
    assert urls == ["https://example.com"]


def test_expand_unknown_pagination_type():
    meta = {
        "start_urls": ["https://example.com"],
        "pagination": {"type": "unknown"}
    }

    urls = expand_paginated_urls(meta)
    assert urls == ["https://example.com"]
