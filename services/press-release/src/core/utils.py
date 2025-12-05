import hashlib

def stable_id(url: str) -> str:
    return hashlib.md5(url.encode()).hexdigest()
