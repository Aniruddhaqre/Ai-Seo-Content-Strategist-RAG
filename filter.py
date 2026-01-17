from urllib.parse import urlparse
from collections import defaultdict
import re

# =========================
# CONFIGURABLE RULE SET
# =========================

INCLUDE_PATTERNS = [
    r"/blog",
    r"/guide",
    r"/learn",
    r"/resource",
    r"/article",
    r"/insights",
    r"/knowledge",
]

EXCLUDE_PATTERNS = [
    r"/tag/",
    r"/category/",
    r"/author/",
    r"/page/",
    r"/wp-",
    r"/login",
    r"/signup",
    r"/privacy",
    r"/terms",
    r"/policy",
    r"/cookie",
    r"/search",
    r"/feed",
    r"\.pdf$",
    r"\.jpg$",
    r"\.png$",
    r"\.webp$",
    r"\.svg$",
]

MAX_URL_DEPTH = 4
MIN_PATH_LENGTH = 2

# =========================
# HELPERS
# =========================

def url_depth(url: str) -> int:
    path = urlparse(url).path.strip("/")
    if not path:
        return 0
    return len(path.split("/"))

def has_query_params(url: str) -> bool:
    return "?" in url or "&" in url

def match_any(patterns, url):
    return any(re.search(p, url.lower()) for p in patterns)

# =========================
# CORE FILTER FUNCTION
# =========================

def filter_urls(urls: list[str]) -> list[str]:
    filtered = []

    for url in urls:
        url = url.strip()

        # Basic sanitation
        if not url.startswith("http"):
            continue

        # Exclude query param pages
        if has_query_params(url):
            continue

        # Depth check
        if url_depth(url) > MAX_URL_DEPTH:
            continue

        # Exclude patterns
        if match_any(EXCLUDE_PATTERNS, url):
            continue

        # Must match include pattern
        if not match_any(INCLUDE_PATTERNS, url):
            continue

        # Path length sanity
        if len(urlparse(url).path.strip("/")) < MIN_PATH_LENGTH:
            continue

        filtered.append(url)

    # Deduplicate
    return list(set(filtered))



MAX_URL_LENGTH = 80

def advanced_filter(urls):
    refined = []

    for url in urls:
        if len(url) > MAX_URL_LENGTH:
            continue

        if any(x in url.lower() for x in ["2020","2021","2019","amp","print","mobile"]):
            continue

        refined.append(url)

    return refined



def limit_per_folder(urls, limit=100):
    folder_map = defaultdict(list)

    for url in urls:
        path = urlparse(url).path.strip("/")
        folder = path.split("/")[0] if "/" in path else path
        folder_map[folder].append(url)

    final = []

    for folder, items in folder_map.items():
        final.extend(items[:limit])

    return final

